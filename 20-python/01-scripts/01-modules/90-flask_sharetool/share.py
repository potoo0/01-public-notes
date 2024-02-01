import os
import time
from flask import (
    Flask, render_template,
    request,
    url_for, redirect, send_from_directory,
    flash,
    make_response, jsonify,
    Response
)
from functools import wraps
from datetime import datetime, timedelta

import psutil
from pprint import pprint


def fix_werkzeug_logging():
    from werkzeug.serving import WSGIRequestHandler

    def address_string(self):
        # nginx config 配置: proxy_set_header X-Real-IP $remote_addr;
        return self.headers.get('X-Real-Ip', self.client_address[0])
    WSGIRequestHandler.address_string = address_string


def docache(minutes=5, content_type='application/json; charset=utf-8'):
    """ Flask decorator that allow to set Expire and Cache headers. """
    def fwrap(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            r = f(*args, **kwargs)
            then = datetime.now() + timedelta(minutes=minutes)
            # rsp = Response(r, content_type=content_type)
            rsp = Response(r)
            rsp.headers.add(
                'Expires',
                then.strftime("%a, %d %b %Y %H:%M:%S GMT"))
            rsp.headers.add(
                'Cache-Control',
                'public,max-age=%d' % int(60 * minutes))
            return rsp
        return wrapped_f
    return fwrap


def get_netcard():
    """获取本机所有网卡的 ip"""
    netcard_info = []
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in v:
            if item[0] == 2 and item[1] != '127.0.0.1':
                netcard_info.append((k, item[1]))
    return netcard_info


# 共享文件夹的根目录
public_root = r'E:\SHARE'
upload_root = r'E:\SHARE\upload'
share_text = r'E:\SHARE\0-text.txt'


app = Flask(__name__)
# 加密 flash 消息
app.secret_key = 'secret'
app.config['PUBLIC_PATH'] = public_root
app.config['UPLOADED_PATH'] = upload_root
app.config['SHARE_TEXT'] = share_text


@app.route('/')
def index():
    return redirect(url_for(".public"))


@app.route('/index')
def public():
    subdir = request.args.get("subdir", '')
    # if subdir:
    if subdir.endswith('..'):
        path = subdir.split(os.sep + '..')[0]
        subdir = os.path.split(path)[0]

    fullpath = os.path.join(app.config['PUBLIC_PATH'], subdir)
    flash({'fullpath': fullpath})

    #  如果是文件，则下载
    if os.path.isfile(fullpath):
        return redirect(url_for('downloader', fullname=fullpath))

    # 列出当前目录下的内容
    content_list = os.listdir(fullpath)
    content_list.sort()
    # 列出目录或文件的信息
    infolist = []
    maxidx = len(content_list)
    for idx, content in enumerate(content_list):
        contentpath = os.path.join(fullpath, content)

        info = {}
        # 如果是目录，在后面添加一个间隔符
        if os.path.isdir(contentpath):
            info['filename'] = content + os.sep
            info['idx'] = idx
        else:
            info['filename'] = content
            info['idx'] = idx + maxidx

        info['mtime'] = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(os.stat(contentpath).st_mtime))

        info['size'] = str(round(os.path.getsize(contentpath) / 1024)) + 'k'
        infolist.append(info)
    infolist.sort(key=lambda dic: dic.get('idx'))
    # flash(infolist)

    return render_template(
        'share.html',
        contents=infolist,
        subdir=subdir,
        ossep=os.sep
    )


@app.route('/download')
def downloader():
    fullname = request.args.get("fullname", '')
    if not fullname:
        return redirect(url_for(".public"))
    filepath, filename = os.path.split(fullname)
    return send_from_directory(
        filepath, filename,
        as_attachment=True)


@app.route('/upload', methods=['POST'])
def upload():
    for f in request.files.getlist('file'):
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    data = {'message': 'upload sucess', 'code': 'SUCCESS'}
    return make_response(jsonify(data), 200)


@app.route('/sharetext', methods=['POST'])
def sharetext():
    data = request.json.get('data')
    with open(app.config['SHARE_TEXT'], 'w', encoding='utf-8') as f:
        f.write(data)
    data = {'message': 'text sync sucess', 'code': 'SUCCESS', 'data': data}
    return make_response(jsonify(data), 200)


@app.route('/readtext', methods=['GET', 'POST'])
def readtext():
    data = ''
    filename = app.config['SHARE_TEXT']
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
    except FileNotFoundError:
        open(filename, 'a').close()
    data = {'message': 'text sync sucess', 'code': 'SUCCESS', 'data': data}
    return make_response(jsonify(data), 200)


if __name__ == '__main__':
    pprint(get_netcard())
    fix_werkzeug_logging()
    app.run(host='127.0.0.1', port=8050, debug=False)
