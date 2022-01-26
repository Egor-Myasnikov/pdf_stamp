import sys
import traceback
from zipfile import ZipFile

from flask import render_template, request, send_from_directory, flash

from app import config
from app import file_work
from app import pdf
from app import create_app

app = create_app()


@app.route("/")
def index():
    return render_template('form.html')


@app.route("/merge_it", methods=['POST'])
def merge_it():
    if request.method == 'POST':

        file_work.remove_old_folders()
        uniq_folder_path = file_work.create_new_folder()

        delom_file_path = None
        if file_work.check_file('delom'):
            delom_file_path = file_work.save_file(uniq_folder_path, request.files['delom'])
            app.logger.info(f'delom - {delom_file_path}')
        else:
            flash('delom file is not delom')

        if file_work.check_file('pdf'):
            pdf_file_path = file_work.save_file(uniq_folder_path, request.files['pdf'])
            app.logger.info(f'pdf - {pdf_file_path}')
        else:
            flash('pdf file is not pdf')

        if delom_file_path:
            try:
                with ZipFile(delom_file_path, 'r') as zip_ref:
                    zip_ref.extractall(uniq_folder_path)
                app.logger.info(f'delom extracted')

                stamps = pdf.prepare_xml(uniq_folder_path.joinpath('delom.xml'))
                tmp_str = render_template(f'clear_pdf.html',
                                          pages=stamps,
                                          uniq_folder_path=app.config['BASEDIR'] / uniq_folder_path,
                                          scale_x=config.SCALE_X, scale_y=config.SCALE_Y)

                stamp_pdf_path = uniq_folder_path.joinpath('out.pdf')
                pdf.save_stamp_pdf(tmp_str, stamp_pdf_path)

                merged_pdf_path = uniq_folder_path.joinpath(f'{pdf_file_path.stem}_stamp{pdf_file_path.suffix}')
                pdf.merge_pdf(pdf_file_path, stamp_pdf_path, merged_pdf_path)

                app.logger.info(f'send pdf')
                return send_from_directory(app.config['BASEDIR'].joinpath(uniq_folder_path),
                                       path=merged_pdf_path.name,
                                       as_attachment=True)
            except:
                exc_type, exc_value, exc_tb = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_tb)
                flash(traceback.format_exception(exc_type, exc_value, exc_tb))

        return render_template('err.html')


if __name__ == "__main__":
    app.run()