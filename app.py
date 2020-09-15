from flask import Flask,render_template,send_from_directory,request,jsonify
from pathlib import Path
from forms import AnalysisForm
import time
import subprocess
import json
from flask_mail import Mail,Message #邮件模块
#flaskAPP设置部分
app = Flask(__name__, static_url_path='/EnDSM',static_folder='static')
app.secret_key = 'c101'#设置网站表单的传输密钥，保证安全
app.config['MAX_CONTENT_LENGTH'] = 5*1024*1024 #将网站允许的最大文件设置为5MB，防止拖垮网站
app.config['UPLOAD_PATH'] = Path(app.root_path).joinpath('files/uploads') #设置网站上传文件的路径
app.config['RESULT_PATH'] = Path(app.root_path).joinpath('files/pred_result') #设置预测结果路径
Path(app.config['UPLOAD_PATH']).mkdir(exist_ok=True, parents=True) #避免因目录不存在而报错
Path(app.config['RESULT_PATH']).mkdir(exist_ok=True, parents=True)




#路由处理部分
@app.route('/EnDSM/')
# @app.route('/EnDSM/index/')
def home():
    form = AnalysisForm()
    return render_template('index.html', form=form)




@app.route('/test2/')
def test2():
    import numpy as np
    data = np.genfromtxt(Path(app.config['RESULT_PATH']).joinpath('out100.vcf'),delimiter='\t', dtype=str)
    _lendata = len(data)

    return render_template('test2.html',resultdata= json.dumps(data.tolist()),resultdatalen=_lendata)



@app.route('/EnDSM/help/')
def help():
    data = '16	74923602	.	G	T	0.83789,17	3372174	.	T	G	0.34289,2	143798008	.	A	G	0.29631,2	21237358	.	C	T	0.28993 ' \
           ',4	89358907	.	C	A	0.286,2	223553175	.	C	G	0.1985,1	206634459	.	T	C	0.22811,1	206634459	.	T	A	0.27093,12	70003893	.	C	T	0.27845,17	17050662	.	T	C	0.18676,1	170015905	.	T	G	0.24871,5	126993369	.	T	A	0.30148,X	109695939	.	A	G	0.32426,1	170015905	.	T	C	0.21218'

    out_data = []
    for line in data.split(','):
        out_data.append(line.split('\t'))

    return render_template('help.html',data=out_data)


def send_email(subject, to, body, resultfile=''):
    message = Message(subject, recipients=[to], body=body)
    with app.open_resource(resultfile) as fp:  # 添加附件
        message.attach(filename=resultfile.name, content_type='text/plain', data=fp.read())  # filename为重命名附件的名字
    mail.send(message)

def excuteCommand(com):
    ex = subprocess.Popen(com, stdout=subprocess.PIPE, shell=True)
    out, err  = ex.communicate()
    ex.wait()
#    print("cmd in:", com)
#    print("cmd out: ", out.decode())
    return out


def findMutation(mutationPath, resultfilePath):
    fileList = []
    header = 'chr	pos	id	ref	alt	EnDSM'
    with open(mutationPath, 'r') as f1, \
        open(resultfilePath, 'w') as f2:
        f2.write(header + '\n')
        for muta in f1:
            muta = muta.strip('\n').split('\t')
            # print(muta)
            cmdStr = 'tabix /data1/wanghuadong/EnDSM/796model_all_syn_score_sort.vcf.gz ' + str(
                muta[0]) + ':' + str(muta[1]) + '-' + str(muta[1])
            result = excuteCommand(cmdStr).decode('ISO-8859-1')
            for line in result.split('\n'):
                _line = line.split('\t')
                if _line[0:5] == muta:
                    fileList.append(_line)
                    f2.write(str(line) + '\n')
    return fileList


@app.route('/EnDSM/analysis')
def analysisIndex():
    form = AnalysisForm()
    return render_template('analysis.html', form=form)




@app.route('/EnDSM/analysisSubmit', methods=['GET', 'POST'])
def analysisSubmit():
    form = AnalysisForm()
    mutation = form.data.data
    nowtime = str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
    filename = nowtime+'.vcf'
    mutationPath = Path(app.config['UPLOAD_PATH']).joinpath(filename)
    with open(mutationPath, 'w') as f:
        for line in mutation.split('\n'):
            f.write(line)
    resultfilePath = Path(app.config['RESULT_PATH']).joinpath(filename)#返回全路径

    fileList = findMutation(mutationPath, resultfilePath)#查询突变

    if form.email.data:
        mail_addr = form.email.data
        with open(Path(app.config['RESULT_PATH']).joinpath('email.txt'),'a') as f:#记录情况
            f.write('{}\t{}\n'.format(mail_addr,nowtime))
        Subject = 'EnDSM analysis' #发信主题
        Recipients = mail_addr #收件人
        web = 'http://bioinfo.ahu.edu.cn/EnDSM/downResult?filename='+filename
        Body = 'Dear '+str(Recipients)+',\n\nYour EnDSM analysis has been completed.\n '+web+'\nPlease refer to the attachment.\n\nThank for using EnDSM.\n\n'+ str(time.strftime("%Y-%m-%d", time.localtime()))#邮件内容
        send_email(subject=Subject,to=Recipients,body=Body,resultfile=resultfilePath)

    return render_template('result.html', filename=filename, resultdata= json.dumps(fileList),resultdatalen=len(fileList))





@app.route('/EnDSM/downResult')
def downResult():
    filename = request.args.get('filename')
    return send_from_directory(str(app.config['RESULT_PATH']),filename=filename,as_attachment=True)#redirect(url_for('/dbDSMv2/'+filename))



@app.route('/EnDSM/download')
def download():

    return render_template('download.html')





#页面错误处理部分
@app.errorhandler(404)#定义404页面
def page_not_found(e):
    return render_template('errors/404.html'),404

@app.errorhandler(413)#定义413页面,文件大于5MB报错
def page_not_found(e):
    return render_template('errors/413.html'),413



if __name__ == '__main__':
    # 邮箱设置
    app.config.update(
        MAIL_SERVER='smtp.aliyun.com',  # smtp服务器
        # MAIL_USE_TLS=True,
        MAIL_PORT=25,  # 不加密的为25端口
        MAIL_USERNAME='xialab@aliyun.com',
        MAIL_PASSWORD='hello.c101',
        MAIL_DEFAULT_SENDER=('EnDSM', 'xialab@aliyun.com')  # 第一个为发件人名字，可自由设置，第二个为发件邮箱
    )
    # 实例化对象
    mail = Mail(app)

    # app.run(debug=True, port=5010, host='210.45.212.94')
    app.run(debug=True,port=5010,host='172.19.8.65')#host='0.0.0.0',