"""Versioned archive of ALL generated art; Owner approval is a separate action.

Full scenes are references, not transparent character sprites. Keep this index
separate from asset_index.json so legacy sprite compositing remains unchanged.
"""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
LIBRARY=ROOT/'character_library'
POLICY={'schema_version':1,'tool':'image_gen','mode':'generate_new_per_scene',
        'archive_every_result':True,'reuse_existing_scene_art_by_default':False,
        'reference_library':'character_library/generated_references',
        'approval_required_before_render':True,'fallback':'stop_and_report_tool_unavailable'}

def now():return datetime.now(timezone.utc).isoformat()

def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def component(value):
    if not isinstance(value,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,119}',value) or '..' in value:
        raise ValueError('Invalid archive path component')
    return value

def archive_root(library):
    library=Path(library).resolve()
    root=library/'generated_references'
    if root.is_symlink():raise ValueError('Archive must not be symlinked')
    root.mkdir(parents=True,exist_ok=True)
    return root

@contextmanager
def locked(library):
    root=archive_root(library)
    fd=os.open(str(root/'index.lock'),os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW,0o600)
    try:
        fcntl.flock(fd,fcntl.LOCK_EX)
        yield root
    finally:os.close(fd)

def load(root):
    p=root/'index.json'
    if p.is_symlink():raise ValueError('Index must not be symlinked')
    return json.loads(p.read_text()) if p.exists() else []

def save(root,rows):
    fd,name=tempfile.mkstemp(prefix='index.',suffix='.part',dir=str(root))
    try:
        with os.fdopen(fd,'w') as f:
            json.dump(rows,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
        os.replace(name,root/'index.json')
    finally:
        if Path(name).exists():Path(name).unlink()

def entries(library=LIBRARY):
    with locked(library) as root:return load(root)

def archive(*,library=LIBRARY,episode,revision,scene,image,prompt,tool='image_gen',characters=None,references=None):
    library=Path(library).resolve()
    episode,revision,scene=map(component,(episode,revision,scene))
    if not isinstance(prompt,str) or not prompt.strip():raise ValueError('Generation prompt required')
    if not isinstance(tool,str) or not tool.strip():raise ValueError('Tool provenance required')
    source=Path(image).resolve()
    with Image.open(source) as im:
        if im.format!='PNG':raise ValueError('Archive source must be original PNG')
        size=list(im.size);mode=im.mode;im.verify()
    sha=digest(source)
    aid='GEN_'+episode+'_'+revision+'_'+scene+'_'+sha[:16]
    with locked(library) as root:
        rows=load(root)
        existing=next((r for r in rows if r['asset_id']==aid),None)
        if existing:
            if digest(Path(library)/existing['image_path'])!=sha:raise ValueError('Archived image changed')
            return existing
        dest=root/episode/revision
        if (root/episode).is_symlink() or dest.is_symlink():
            raise ValueError('Archive subfolders must not contain symlinks')
        dest.mkdir(parents=True,exist_ok=True)
        if dest.resolve()!=dest.absolute():raise ValueError('Archive subfolders must not contain symlinks')
        path=dest/(scene+'__'+sha[:16]+'.png')
        if path.is_symlink():raise ValueError('Archived file must not be symlinked')
        # Exclusive creation preserves every previous variant, including rejected ones.
        if not path.exists():
            with source.open('rb') as src,path.open('xb') as dst:
                for chunk in iter(lambda:src.read(1048576),b''):dst.write(chunk)
        if digest(path)!=sha:raise ValueError('Archive copy checksum mismatch')
        record={'asset_id':aid,'asset_category':'generated_reference','source_episode':episode,
                'source_revision':revision,'scene':scene,'image_path':str(path.relative_to(Path(library))),
                'source_image':str(source),'sha256':sha,'pixel_size':size,'mode':mode,'tool':tool,
                'prompt':prompt,'reference_inputs':references or [],'characters':characters or [],
                'approval_status':'pending_owner_review','approved_for_reuse':False,
                'created_at':now(),'review_history':[]}
        rows.append(record);save(root,rows)
        return record

def review(library,asset_ids,status,evidence):
    if status not in ('approved','rejected','pending_owner_review') or not evidence.strip():
        raise ValueError('Explicit review evidence and supported status required')
    with locked(library) as root:
        rows=load(root);selected=[r for r in rows if r['asset_id'] in asset_ids]
        if {r['asset_id'] for r in selected}!=set(asset_ids):raise ValueError('Unknown asset ID')
        for r in selected:
            if digest(Path(library)/r['image_path'])!=r['sha256']:raise ValueError('Review image checksum mismatch')
        for r in selected:
            event={'status':status,'evidence':evidence,'sha256':r['sha256'],'at':now()}
            r['review_history'].append(event)
            r.update(approval_status=status,approved_for_reuse=status=='approved',updated_at=event['at'])
        save(root,rows)
        return selected

def search(library=LIBRARY,query='',approved_only=True):
    words=query.casefold().split()
    out=[]
    for r in entries(library):
        if approved_only and r['approval_status']!='approved':continue
        text=' '.join([r['source_episode'],r['scene'],r['prompt']]+r['characters']).casefold()
        if not all(w in text for w in words):continue
        if digest(Path(library)/r['image_path'])!=r['sha256']:raise ValueError('Reference checksum mismatch')
        out.append(r)
    return out

def import_manifest(path,episode,revision,library=LIBRARY):
    path=Path(path).resolve();m=json.loads(path.read_text());records=[]
    for r in m['images']:
        source=(path.parent/r['saved_file']).resolve()
        if path.parent not in source.parents:raise ValueError('Manifest image escapes revision folder')
        records.append(archive(library=library,episode=episode,revision=revision,scene=r['scene'],
            image=source,prompt=r['prompt'],tool=r['tool'],characters=['ti','ngang','mimi'],
            references=r.get('references',[])))
    return records

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--library',type=Path,default=LIBRARY)
    sub=ap.add_subparsers(dest='cmd',required=True)
    p=sub.add_parser('art-add');p.add_argument('image',type=Path)
    for key in ('episode','revision','scene','prompt-file'):p.add_argument('--'+key,required=True)
    p=sub.add_parser('art-import');p.add_argument('manifest',type=Path)
    for key in ('episode','revision'):p.add_argument('--'+key,required=True)
    p=sub.add_parser('art-review');p.add_argument('asset_ids',nargs='+')
    p.add_argument('--status',choices=['approved','rejected','pending_owner_review'],required=True)
    p.add_argument('--evidence',required=True)
    p=sub.add_parser('references');p.add_argument('query',nargs='*');p.add_argument('--include-pending',action='store_true')
    args=ap.parse_args(argv)
    if args.cmd=='art-add':
        spec=json.loads(Path(args.prompt_file).read_text())
        rows=[archive(library=args.library,episode=args.episode,revision=args.revision,scene=args.scene,
            image=args.image,prompt=spec['prompt'],tool=spec.get('tool','image_gen'),
            characters=spec.get('characters',[]),references=spec.get('references',[]))]
    elif args.cmd=='art-import':rows=import_manifest(args.manifest,args.episode,args.revision,args.library)
    elif args.cmd=='art-review':rows=review(args.library,args.asset_ids,args.status,args.evidence)
    else:rows=search(args.library,' '.join(args.query),not args.include_pending)
    print(json.dumps(rows,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
