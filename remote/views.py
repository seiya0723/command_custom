from django.shortcuts import render,redirect
from django.views import View

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse

from django.conf import settings 

from .models import History 
from .forms import HistoryForm

import subprocess,sys

        
import glob,datetime,os

class IndexView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):

        context                 = {}
        context["histories"]    = History.objects.order_by("-dt")


        #=======実行するスクリプトの一覧を表示====================

        files = glob.glob("./scripts/*")

        file_list = []
        date_list = []
        
        for file in files:
            p = file
            t = os.path.getmtime(p)
            d = datetime.datetime.fromtimestamp(t)
            file_list.append(p)
            date_list.append(d)


        context["file_list"]    = file_list
        context["date_list"]    = date_list

        #====================================================




        return render(request,"remote/index.html",context)

    def post(self, request, *args, **kwargs):

        json_data   = { "error":True }

        #=======実行するスクリプトの一覧を表示====================

        files = glob.glob("./scripts/*")
        file_list = []
        
        for f in files:
            file_list.append(f)

        #====================================================




        #===========ここで送信されたコマンドのチェックをする=====================

        form    = HistoryForm(request.POST)

        #不適切な文字列(コマンドの連続実行に使える&や|など)をチェックする。含んでいれば許可しない
        if not form.is_valid():
            messages.info(request, form.errors)
            #return redirect("remote:index")

            return JsonResponse(json_data)

        print("OK")

        clean   = form.clean()
        command = clean["command"]

        #冒頭の空白を除去、リスト型に変換。最初のコマンドをチェックする
        command_list    = command.strip().split(" ")

        #このパターンはありえないが、models.py及びforms.pyの仕様が変わるとありえるパターンなので設置
        if len(command_list) == 0:
            messages.info(request, "エラー")
            #return redirect("remote:index")

            return JsonResponse(json_data)
        

        #HACK:添字を直指定している。できれば要修正
        #if command_list[0] not in settings.ALLOW_COMMAND_LIST:
        if command_list[0] not in file_list:
            messages.info(request, "このコマンドは許可されていません")
            #return redirect("remote:index")

            return JsonResponse(json_data)

        #===========ここで送信されたコマンドのチェックをする=====================

        #============ここでコマンドを実行する============

        #shell=Trueにすると、&&を実行したり、cdコマンドが実行できる(※ただし文字列型にして引き渡しをする必要が有る。)
        #stdout=subprocess.PIPEを指定して実行結果を出力できるようにする。
        cp      = subprocess.run(command , stdout=subprocess.PIPE ,shell=True)

        if cp.returncode != 0:
            messages.info(request, "コマンドの実行に失敗しました")
            #return redirect("remote:index")

            return JsonResponse(json_data)

        #UTF-8でデコードしないと日本語が文字化けする。
        print(cp.stdout.decode("utf-8"))
        messages.info(request, cp.stdout.decode("utf-8"))
        form.save()

        #============ここでコマンドを実行する============

        #Ajaxはjsonで返すように行っているので、jsonでレスポンスをする。JsonResponseを使えば、指定した辞書型がJSON形式でレスポンスされる。
        #return redirect("remote:index")

        #TODO:ここで別テンプレート化させたHTMLをレンダリング、HTML文字列を辞書データに格納してJsonResponseとする。受け取ったJavaScript側は.html()でHTMLを貼り付ける。render_to_string()を使用する。
        json_data["error"]      = False


        return JsonResponse(json_data)

index   = IndexView.as_view()

