import uuid
import datetime

from pathlib import Path
from werkzeug.utils import secure_filename
from flask import request, flash

from app import config


def allowed_file(filename, file_type):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_FILE_TYPE[file_type]


def check_file(file_type):
    if file_type not in request.files:
        flash(f'No {file_type} file')
        # logging.Logger.info(f'no file {file_type}')
        return False

    file = request.files[file_type]
    if file.filename == '':
        flash(f'No selected file {file_type}')
        # logging.Logger.info(f'No selected file {file_type}')
        return False

    return file and allowed_file(file.filename, file_type)


def save_file(path, file):
    filename = secure_filename(file.filename)
    returned_path = path.joinpath(filename)
    file.save(str(returned_path))
    return returned_path


def create_new_folder():
    today_folder = datetime.date.today().strftime('%d_%m_%Y')
    Path(config.UPLOAD_FOLDER).joinpath(today_folder).mkdir(exist_ok=True)

    uniq_folder = str(uuid.uuid4())
    uniq_folder_path = Path(config.UPLOAD_FOLDER).joinpath(today_folder).joinpath(uniq_folder)
    uniq_folder_path.mkdir(exist_ok=True)
    return uniq_folder_path


def remove_old_folders():
    directory = Path(config.UPLOAD_FOLDER)
    for dir in directory.iterdir():
        try:
            date = datetime.datetime.strptime(dir.name, "%d_%m_%Y")
            deleted = datetime.date.today() - date.date() > datetime.timedelta(config.BACKUP_PERIOD)
        except:
            deleted = True

        if deleted:
            rm_tree(dir)


def rm_tree(pth):
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)

    if pth.is_file():
        pth.unlink()
    else:
        pth.rmdir()
