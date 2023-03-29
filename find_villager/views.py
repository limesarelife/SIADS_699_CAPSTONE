from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .forms import VillagerForm
from .python_scripts_villagers import info_ret_sys_lsi, info_ret_sys_wemb

# Create your views here.
def home_view(request):
    if request.method == 'POST':
        form = VillagerForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            
            # print(form.cleaned_data)
            user_dict = form.cleaned_data
            user_list_this = list(user_dict.values())[1:11]
            print(user_list_this)

            user_sim_cl = info_ret_sys_lsi.RetrievalSystem(path_file = ("./python_scripts_villagers/"), num_topics=9,
                              user_list = user_list_this
                              )
            user_sim_cls = info_ret_sys_wemb.RetrievalSystem_wb(path_file = ("./python_scripts_villagers/"),
                                user_list = user_list_this
                              )
            

            villager_1, villager_2 = user_sim_cl.retrieve_n_rank_docs()
            v_id1, v_id2 = user_sim_cl.get_villagers_id(vil_1 = villager_1, vil_2 = villager_2)
            v_name1, v_img1 = user_sim_cl.return_image(v_id1, v_id2)
            

            villager_sim = user_sim_cls.get_cossim_villagers()
            v_id1, v_id2 = user_sim_cls.finalize_sim_villagers(villager_sim)
            v_name2, v_img2 = user_sim_cls.return_image(v_id1, v_id2)
            
            vil_info : dict = {"Option_1":v_name1,"Villager_1":v_img1 ,"Option_2":v_name2, "Villager_2": v_img2}
            # print(vil_info)
            return redirect(reverse('find_villager_home_app:final_vil',kwargs=vil_info))
        else:
            # print(form.cleaned_data)
            
            return HttpResponse("Please fill out all questions.")
    # print(request.POST)
    return render(request, 'find_villager/index.html')

def final_villager(request, **kwargs):
    print(kwargs)
    return render(request, 'find_villager/results.html')


