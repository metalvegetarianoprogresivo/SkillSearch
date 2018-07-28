import os
from django.conf import settings
from django.shortcuts import redirect, render, reverse
from docx import Document
from .forms import GetDocumentsForm
from .get_documents import GetDocumentsCommand
from .models import Bio, Technical

def index(request):
    context = {
    }
    return render(request, 'bios/index.html', context)

def process_documents():
    for file_name in filter(
        lambda s: s.endswith('.docx') and '~' not in s,
        os.listdir(settings.BIOS_ROOT)
    ):
        print('Updating: {}'.format(file_name))
        with open(os.path.join(settings.BIOS_ROOT, file_name), 'rb') as resume:
            document = Document(resume)
        bio = Bio()
        profile_flag = technical_flag = 0

        for row in document.tables[0].rows:
            for count, cell in enumerate(row.cells):
                cell_text = cell.text.strip()
                if cell_text and not bio.name:
                    bio, created = Bio.objects.get_or_create(
                        name=cell_text
                    )
                elif cell_text and not bio.title and cell_text != bio.name:
                    bio.title = cell_text
                else:
                    if profile_flag:
                        profile_flag = 0
                        bio.profile = cell_text
                    elif technical_flag:
                        if cell_text:
                            if cell_text.lower() == 'education':
                                technical_flag = 0
                                continue
                            if '\n' in cell_text:
                                skills = map(str.strip, cell_text.split('\n'))
                                for name in filter(
                                    lambda s: len(s) and len(s) < 31,
                                    skills
                                ):
                                    if "/" in name:
                                        for sub in name.split("/"):
                                            skill, _ = Technical.objects.get_or_create(
                                                name=sub.strip()
                                            )
                                            try:
                                                bio.technical_skills.add(skill)
                                            except:
                                                # Skill already added
                                                continue
                                    else:
                                        skill, _ = Technical.objects.get_or_create(
                                            name=name
                                        )
                                        try:
                                            bio.technical_skills.add(skill)
                                        except:
                                            # Skill already added
                                            continue
                            elif len(cell_text) < 31:
                                if "/" in name:
                                    for sub in name.split("/"):
                                        skill, _ = Technical.objects.get_or_create(
                                            name=sub.strip()
                                        )
                                        try:
                                            bio.technical_skills.add(skill)
                                        except:
                                            # Skill already added
                                            continue
                                else:
                                    skill, _ = Technical.objects.get_or_create(
                                        name=cell_text
                                    )
                                    try:
                                        bio.technical_skills.add(skill)
                                    except:
                                        # Skill already added
                                        continue
                    if cell_text.lower() == 'profile':
                        profile_flag = 1
                    elif cell_text.lower() == 'technical':
                        technical_flag = 1

        if not bio.profile:
            for row in document.tables[0].rows:
                for cell in row.cells:
                    for t in cell.tables:
                        for r in t.rows:
                            for c in filter(lambda i: i.text, r.cells):
                                text = c.text.strip()
                                if text not in bio.profile:
                                    bio.profile += '\n{}'.format(text)
        bio.save()

def get_documents(request):
    if request.method == 'POST':
        form = GetDocumentsForm(request.POST)
        if form.is_valid():
            command = GetDocumentsCommand(
                form.cleaned_data['email'],
                form.cleaned_data['password']
            )
            command.handle()
            if not command.error:
                process_documents()
                return redirect('bios_index')
            else:
                form.add_error('email', command.error)
    else:
        form = GetDocumentsForm()

    context = {
        'title': 'Update Bios',
        'form': form,
        'form_action': reverse('get_documents')
    }

    return render(request, 'bios/form.html', context)
