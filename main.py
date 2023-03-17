

import os
import shutil
from tqdm import tqdm


current_dir = os.getcwd()
template_dir = os.path.join("D:/env/template/templates")


def copyfileobj(fsrc, fdst, callback, length=0):
    try:
        # check for optimisation opportunity
        if "b" in fsrc.mode and "b" in fdst.mode and fsrc.readinto:
            return _copyfileobj_readinto(fsrc, fdst, callback, length)
    except AttributeError:
        # one or both file objects do not support a .mode or .readinto attribute
        pass

    if not length:
        length = shutil.COPY_BUFSIZE

    fsrc_read = fsrc.read
    fdst_write = fdst.write

    copied = 0
    while True:
        buf = fsrc_read(length)
        if not buf:
            break
        fdst_write(buf)
        copied += len(buf)
        callback(copied)


# differs from shutil.COPY_BUFSIZE on platforms != Windows
READINTO_BUFSIZE = 1024 * 1024


def _copyfileobj_readinto(fsrc, fdst, callback, length=0):
    """readinto()/memoryview() based variant of copyfileobj().
    *fsrc* must support readinto() method and both files must be
    open in binary mode.
    """
    fsrc_readinto = fsrc.readinto
    fdst_write = fdst.write

    if not length:
        try:
            file_size = os.stat(fsrc.fileno()).st_size
        except OSError:
            file_size = READINTO_BUFSIZE
        length = min(file_size, READINTO_BUFSIZE)

    copied = 0
    with memoryview(bytearray(length)) as mv:
        while True:
            n = fsrc_readinto(mv)
            if not n:
                break
            elif n < length:
                with mv[:n] as smv:
                    fdst.write(smv)
            else:
                fdst_write(mv)
            copied += n
            callback(copied)


def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


def ignore_git_files(src_folder, dst_folder, progress_bar=None):
    ignore_list = []
    if os.path.exists('.gitignore'):
        with open('.gitignore') as f:
            ignore_list = [line.strip() for line in f if line.strip()
                           and not line.startswith('#')]

    for item in os.listdir(src_folder):
        src_path = os.path.join(src_folder, item)
        dst_path = os.path.join(dst_folder, item)

        if item in ignore_list:
            continue

        if os.path.isdir(src_path):
            os.makedirs(dst_path, exist_ok=True)
            ignore_git_files(src_path, dst_path, progress_bar=progress_bar)
        else:
            if progress_bar:
                progress_bar.set_description(os.path.basename(src_path))
                with open(src_path, 'rb') as src_file, \
                        open(dst_path, 'wb') as dst_file, \
                        tqdm(total=os.path.getsize(src_path), unit='B', unit_scale=True) as pbar:
                    copyfileobj(src_file, dst_file, length=64*1024,
                                callback=lambda copied_bytes: pbar.update(copied_bytes - pbar.n))
            else:
                shutil.copy2(src_path, dst_path)


def copy_folder_with_progress(src, dst):
    total = sum([len(files) for root, dirs, files in os.walk(src)])
    with tqdm(total=total, unit='file') as pbar:
        for foldername, subfolders, filenames in os.walk(src):
            for filename in filenames:
                src_file = os.path.join(foldername, filename)
                dst_file = os.path.join(dst, src_file.replace(src, ''))
                if not os.path.exists(os.path.dirname(dst_file)):
                    os.makedirs(os.path.dirname(dst_file))
                shutil.copy2(src_file, dst_file)
                pbar.update(1)


def copy_files(src, dst):
    # check if have .gitignore
    if os.path.exists(os.path.join(src, '.gitignore')):
        ignore_patterns = shutil.ignore_patterns(
            *open(os.path.join(src, '.gitignore')).readlines())
        shutil.copytree(src, dst, ignore=ignore_patterns)
    else:
        shutil.copytree(src, dst)


def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


templates = []
for template in os.listdir(template_dir):
    item_path = os.path.join(template_dir, template)
    if os.path.isdir(item_path):
        templates.append({
            "name": template,
            "path": item_path
        })

print("Select a template to use:")
for i, template in enumerate(templates):
    print(f"{i+1}. {template['name']}")

template_index = int(input("Enter a number: ")) - 1
if (template_index < 0 or template_index >= len(templates)):
    print("Invalid template index")
    exit(1)


template_select = templates[template_index]

print("Project name:", end=" ")
project_name = input()

# create project folder
project_path = os.path.join(current_dir, project_name)


print("Copying template...")
print("Source:", template_select['path'])
print("Destination:", project_path)

# progress_bar = tqdm(total=get_folder_size(
#     template_select['path']), unit='B', unit_scale=True)
# ignore_git_files(template_select['path'], project_path)

copy_files(template_select['path'], project_path)

print("Successfully copied template!")
