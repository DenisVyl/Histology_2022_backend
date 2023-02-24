from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from prj.settings import MEDIA_ROOT


def base_view(request, **kwargs):
    return render(request, 'base.html')


def home_view(request, **kwargs):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        description = request.POST['description']
        email = request.POST['email']
        now = strftime("%Y-%m-%d-%H-%M-%S", localtime())

        folder = email + now

        fs = FileSystemStorage()
        uploaded_file_name = fs.save(
            name=uploaded_file.name, content=uploaded_file)
        context['url'] = fs.url(uploaded_file_name)

        path_to_txt = str(MEDIA_ROOT) + os.sep + folder + os.sep + \
            os.path.splitext(uploaded_file_name)[0] + '.txt'
        print(f'{path_to_txt=}')
        dir = str(MEDIA_ROOT) + os.sep + folder
        subprocess.run(f'mkdir {dir}', shell=True)
        with open(path_to_txt, 'w') as wf:
            wf.write(email + '\n' + description)

        message_now = strftime("%Y-%m-%d, %H:%M:%S", localtime())
        message_text = f'{message_now}, Загружен новый файл'
        print(f'Sending {message_text}')
        send_mail(
            subject=message_text,
            message=message_text,
            from_email=EMAIL_HOST_USER,
            recipient_list=[EMAIL_HOST_USER],
            fail_silently=False,
        )

    return render(request, 'home.html', context)
