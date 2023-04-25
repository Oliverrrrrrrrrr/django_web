from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponseRedirect

from python_function.Qualification.caigouwang_spider import get_cgw_data
from python_function.Qualification.tianyancha_spider import tianyancha_spider
from python_function.Qualification.xyzg_spider import get_creditChina
from python_function.Repeatability.seal_detect.signiture_detect import bianli_pics, pdf2image
from python_function.Repeatability.duplicate_checking.duplicate_paragraph import dup_paragraph
from python_function.Predict.predict import extract_text_info, predict
from .models import User, Project, Main_person, Tianyancha_User, UploadProjectFile, UploadTestFile, \
    Shareholder_information, Seal, Qualification_person, Register_person, Duplicate, CreditChina, CGW_inquire


# index
def index(request):
    return render(request, 'Home.html')


# register
def register(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # 注册成功跳转到到登录页面，注册加判断已经存在提示改用用户已存在
        users = User.objects.all()
        for i in users:
            if username == i.username:
                return HttpResponse("用户名已存在")
        if password == password2:
            try:
                User.objects.create_user(username=username, password=password)
            except Exception as e:
                print(e)
                return HttpResponse("注册失败")
        else:
            return HttpResponse("两次密码不一致")
        return redirect('/login/')


# login
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        # 检查用户名和密码是否正确
        user = User.objects.filter(username=name).first()
        if user is None:
            return HttpResponse("用户名不存在")
        elif not check_password(password, user.password):
            return HttpResponse("密码错误")
        else:
            auth.login(request, user)
            request.session['username'] = name
            resp = HttpResponseRedirect('/')
            if 'remember' in request.POST:
                resp.set_cookie('username', name, 3600 * 24 * 7)
            return resp


# logout
def logout(request):
    # 实现退出功能
    # 删除session
    if 'username' in request.session:
        del request.session['username']
    resp = HttpResponseRedirect('/')
    # 删除cookie
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    auth.logout(request)
    messages.success(request, "已退出登录")
    return resp


# change password
def change_password(request):
    if request.method == 'GET':
        return render(request, 'change_password.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        password3 = request.POST.get('password3')
        try:
            user = User.objects.get(name=name)
        except:
            return HttpResponse("用户名不存在")
        if check_password(password, user.password):
            if password2 == password3:
                password2 = make_password(password2)
                user.password = password2
                user.save()
                return redirect('/login/')
            else:
                return HttpResponse("两次密码不一致")
        else:
            return HttpResponse("原密码错误")


# upload file
def import_data(request):
    if request.method == 'GET':
        return render(request, 'import.html')
    elif request.method == 'POST':
        type = request.POST.get('type')
        if type in ['招标文件', '投标文件']:
            project_name = request.POST.get('project name')
            project_file = request.FILES.get('project file')
            if project_file:
                # 查询是否已上传过该文件
                if UploadProjectFile.objects.filter(title=project_file.name):
                    return HttpResponse("该文件已上传")
                # 保存项目信息
                f = UploadProjectFile(type=type, project_name=project_name, title=project_file.name, path=project_file)
                f.save()
                return render(request, 'import.html', {'msg': '上传成功'})
            else:
                return HttpResponse("上传失败")
        else:
            test_file = request.FILES.get('test file')
            if test_file:
                if UploadTestFile.objects.filter(title=test_file.name):
                    return HttpResponse("该文件已上传")
                f = UploadTestFile(type=type, title=test_file.name, path=test_file)
                f.save()
                return render(request, 'import.html', {'msg': '上传成功'})
            else:
                return HttpResponse("上传失败")


def Qualification(request):
    if request.method == 'GET':
        return render(request, 'Qualification.html')
    elif request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        companyname = request.POST.get('companyname')

        # 天眼查
        # 如果数据库中已经有该企业的数据，就不再爬取
        if not Main_person.objects.filter(company_name=companyname):
            try:
                tianyancha_spider(phone, password, companyname)
            except Exception as e:
                print(e)
                return HttpResponse("天眼查爬取失败")
        # 找到数据库中对应企业的数据
        all_main_person = Main_person.objects.filter(company_name=companyname)
        all_project = Project.objects.filter(company_name=companyname)
        all_shareholder = Shareholder_information.objects.filter(company_name=companyname)
        all_qualification = Qualification_person.objects.filter(company_name=companyname)
        all_register_person = Register_person.objects.filter(company_name=companyname)
        # 采购网（没成功）
        if not CGW_inquire.objects.filter(company_name=companyname):
            try:
                get_cgw_data(companyname)
            except Exception as e:
                print(e)
                return HttpResponse("采购网爬取失败")
        cgw_data = CGW_inquire.objects.filter(company_name=companyname)

        # 信用中国
        if not CreditChina.objects.filter(entityName=companyname):
            try:
                M = get_creditChina(companyname)  # M为信用中国爬取的展示信息（行政信息）
                # 将数据按照下标索引分别传输到HTML页面的td中
                split_data = [M[i:i + 9] for i in range(0, len(M), 9)]

            except Exception as e:
                print(e)
                return HttpResponse("信用中国爬取失败")

        return render(request, 'Qualification.html', {
            'all_main_person': all_main_person,
            'all_project': all_project,
            'all_shareholder': all_shareholder,
            'all_qualification': all_qualification,
            'all_register_person': all_register_person,
            'cgw_data': cgw_data
        })


def Repeatability(request):
    if request.method == 'GET':
        return render(request, 'Repeatability.html')
    elif request.method == 'POST':
        # 印章检测函数接口
        type = request.POST.get('type')
        if type == '印章检测':
            filename = request.POST.get('project name')
            # 查看数据库中是否已有检测结果
            if not Seal.objects.filter(file_title=filename):
                # 调取数据库里的pdf
                try:
                    file = UploadProjectFile.objects.get(title=filename + ".pdf")
                except:
                    return HttpResponse("文件不存在")
                # 未检测过则进行检测
                pdfFile = file.path.path  # 设置pdf路径                
                storePath = r"static/media/Seal_Picture" + "/" + filename  # 设置存储路径
                try:
                    pdf2image(pdfFile, storePath, zoom=2.0)  # pdf转图片
                    bianli_pics(pdfFile, storePath, filename)  # 遍历图片并对有印章的图片进行输出页码和提取

                except Exception as e:
                    print(e)
                    return HttpResponse("检测失败")

            all_seal = Seal.objects.filter(file_title=filename)
            # 将所有页码拼接成字符串
            pages = ""
            page_len = len(all_seal)
            all_pages = []
            for seal in all_seal:
                pages += seal.seal_page + ","
                all_pages.append(seal.seal_page)

            return render(request, 'Repeatability.html',
                          {'all_seal': all_seal, 'pages': pages, 'page_len': page_len, 'all_pages': all_pages})


        # 重复字段检测函数接口
        elif type == '重复字段检测':

            name_list = []
            name_list = []  # 'media/file/project_file/上海浦海测绘有限公司技术部分.pdf', 'media/file/project_file/上海祥阳水利勘测设计有限公司技术部分.pdf']
            start_list = []  # 1,1]
            end_list = []  # 100,30]
            standard_name = []
            standard_start = []
            standard_end = []

            # importing = request.POST.get('importing')           

            # # 查看数据库中是否已有检测结果
            # if not Duplicate.objects.filter(file_pair=name_list):
            # 调取数据库里的pdf
            # try:
            #     file = UploadProjectFile.objects.get(title=name_list[0] + ".pdf")
            # except:
            #     return HttpResponse("文件不存在")
            # 未检测过则进行检测   

            start_number = int(request.POST.get('InputMatchingStringLimit'))
            # start_number = []
            # start_number.append(start_num)

            standard_number = int(request.POST.get('InputLibraryStringLimit'))
            # standard_number = []
            # standard_number.append(standard_num)

            standard_n = request.POST.get('InputStandardLibrary')
            # standard_n = "../file/project_file/" + standard_n#"../../../file/project_file/" + standard_n            
            file = UploadProjectFile.objects.get(title=standard_n + ".pdf")

            L = 'static/media/' + str(file.path)
            standard_name.append(L)

            standard_s = int(request.POST.get('InputStandardStartPage'))
            standard_start.append(standard_s)

            standard_e = int(request.POST.get('InputStandardEndPage'))
            standard_end.append(standard_e)

            # while importing:
            # file_name = request.POST.get('file_name')

            # file = UploadProjectFile.objects.get(title=file_name + ".pdf")
            # M = 'media/'+ str(file.path)
            # name_list.append(M)
            file_name = request.POST.getlist('file_name')
            start_list = request.POST.getlist('InputStartPage')
            end_list = request.POST.getlist('InputEndPage')

            for i in file_name:
                file = UploadProjectFile.objects.get(title=i + ".pdf")
                M = 'static/media/' + str(file.path)
                name_list.append(M)

            for i in range(len(file_name)):
                start_list[i] = int(start_list[i])
                end_list[i] = int(end_list[i])

            # start_page = int(request.POST.get('InputStartPage'))
            # end_page = int(request.POST.get('InputEndPage'))
            # start_list.append(start_page)   #request.POST.getlist('InputStartPage')
            # end_list.append(end_page)

            # name_list = request.POST.getlist('file_name')
            # start_list = request.POST.getlist('InputStartPage')
            # end_list = request.POST.getlist('InputEndPage')                  

            try:
                output_str, contrast_output = dup_paragraph(standard_name, name_list, standard_start, standard_end,
                                                            start_list, end_list, start_number, standard_number)
            except Exception as e:
                print(e)
                return HttpResponse("检测失败")
            return render(request, 'Repeatability.html', {'output_str': output_str, 'contrast_output': contrast_output})


def Predict(request):
    if request.method == 'GET':
        return render(request, 'Predict.html')
    elif request.method == 'POST':
        #需要检测的文件路径（单个）
        file_name = request.POST.get('project name')
        file = UploadProjectFile.objects.get(title=file_name + ".pdf")
        filepath = 'static/media/' + str(file.path)
        # pathlist = []
        # pathlist.append(filepath)
        
        text = extract_text_info(filepath)
        problist = predict(text)

        prob = problist[0] * 100
        return render(request, 'Predict.html', {'prob': prob})

#津耀刻盘