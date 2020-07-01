from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .blur_img.start import BlurCls
import os
import shutil
from datetime import datetime
from .serializers import FileSerializer


class Home(APIView):

    def get(self, request, *args, **kwargs):
        today = datetime.today()
        today = str(today).split(" ")[0]
        exits_dates = os.listdir("backup/")

        if today in exits_dates:
            # print("today exist")
            pass
        else:
            current_files = os.listdir("media/")
            li = [i for i in current_files if i.endswith(".jpg") or i.endswith(".png") or i.endswith(".jpeg")]
            if len(li) > 0:
                date_time = datetime.today()
                date_time = str(date_time).split(" ")[0]
                shutil.copytree("media/", f"backup/{date_time}")
                for i in li:
                    os.remove(f"media/{i}")
                shutil.rmtree("media/results/")

        return render(request, 'home.html')

    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        obj = BlurCls()
        obj.start(f"media/{filename}")

        download_path = f"media/results/blur_{filename}"

        return render(request, 'output.html', {"original": uploaded_file_url, "blur": download_path})
