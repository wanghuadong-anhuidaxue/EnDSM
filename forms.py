# -*- coding: utf-8 -*-
"""
Pycharm Editor
Create by zhwei at 2019/10/6
by whd 2020/7/2
Python：3.7.0
"""


from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField, SelectMultipleField, SelectField#分别对应单行文本，提交，文件上传，多行文本,选择
from flask_wtf.file import FileAllowed,FileRequired,FileField
from wtforms.validators import InputRequired,DataRequired,Length,ValidationError,Email #验证器，分别对应是否输入，是否数据正确，长度限制，邮箱格式是否正确



class AnalysisForm(FlaskForm):
    data = TextAreaField(label='data',id="userInput", render_kw={'placeholder':'Type synonymous mutations as VCF format','class_':"form-control", 'style':'height:120px', 'autocomplete':"off",})
    email = StringField(label='eMail', id='eMail',render_kw={'autocomplete': 'off','class_': 'form-control','placeholder':"Please input Email address"})
    uploaddata = FileField(label='uploaddata', id="uploaddata", render_kw={'class_':'custom-file-input',"multiple data-min-file-count":'1','accept':'.vcf', 'onchange':"getFileName(this.value)","style":"display:none;"})
    submit = SubmitField('Submit',id='submitBtn',render_kw={'onclick':'check_sequence()','class_':'layui-btn'})






# class AdvancedSearchForm(FlaskForm):
#     Gene = SelectField(label='Gene', id='Gene',render_kw={'lay-verify':"required", 'style':'width:17%;margin-left:10%;','class':'layui-nav-item'},)
#     Disease = SelectField(label='Disease', id='Disease',render_kw={'lay-verify':"required", 'style':'width:17%;margin-left:10%;'},)
#     Chromosome = SelectField(label='Chromosome', id='Chromosome',render_kw={'lay-verify':"required", 'style':'width:17%;margin-left:10%;'},)
#     dbDSMScore = SelectField(label='DBDSMScore', id='DBDSMScore',render_kw={'lay-verify':"required", 'style':'width:17%;margin-left:10%;'},)
#     submit2 = SubmitField('Submit', id='submitBtn',
#                          render_kw={'lay-submit': '', 'lay-filter': '*', 'class_': 'layui-btn',
#                                     'style': "background-color: #5FB878;",'onclick':"checkPur()"})
#     reset = SubmitField('Reset', id='resetBtn', render_kw={'class_': 'layui-btn layui-btn-primary', 'type': "reset"})
#
#     def __init__(self, *args, **kwargs):
#         super(AdvancedSearchForm, self).__init__(*args, **kwargs)
#         #Gene
#         self.Gene.choices = [(1, 'Please Select Gene')]
#         results = AllData.query.with_entities(AllData.Gene).distinct().all()
#         results = sorted(results, key=lambda i: i[0])
#         for i, ret in enumerate(results):
#             self.Gene.choices.append((i+2 , ret[0]))
#         #Disease
#         self.Disease.choices = [(1, 'Please Select Disease')]
#         results = AllData.query.with_entities(AllData.Disease).distinct().all()
#         results = sorted(results, key=lambda i: i[0])
#         for i, ret in enumerate(results):
#             self.Disease.choices.append((i + 2, ret[0]))
#         # Chromosome
#         self.Chromosome.choices = [(1, 'Please Select Chromosome')]
#         results = AllData.query.with_entities(AllData.Chromosome).distinct().all()
#         results = sorted(results, key=lambda i: i[0])
#         for i, ret in enumerate(results):
#             self.Chromosome.choices.append((i+2 , ret[0]))
#
#         # dbDSMScore
#         self.dbDSMScore.choices = [(1, 'Please dbDSMScore Chromosome')]
#         results = AllData.query.with_entities(AllData.DBDSMScore).distinct().all()
#         print(results)
#         # results = sorted(results, key=lambda i: i[0])
#         for i, ret in enumerate(results):
#             self.dbDSMScore.choices.append((i+2 , ret[0]))