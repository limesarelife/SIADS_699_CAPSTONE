from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .forms import VillagerForm, VillagerResponse
from .python_scripts_villagers import info_ret_sys_lsi, info_ret_sys_wemb
from .models import VillagerResponseDB
# Create your views here.
def home_view(request):
    if request.method == 'POST':
        form = VillagerForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            
            
            user_dict = form.cleaned_data
            user_list_this = list(user_dict.values())[1:11]
            

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
            v_id1_wemb, v_id2_wemb = user_sim_cls.finalize_sim_villagers(villager_sim)
            v_name2, v_img2 = user_sim_cls.return_image(v_id1_wemb, v_id2_wemb)
            
            vil_info = {"Option_1":str(v_name1),"Villager_1":str(v_img1),
                               "Option_2":str(v_name2),"Villager_2":str(v_img2)}
            
        
            response = redirect(reverse('find_villager_home_app:response_quiz'))
            response.set_cookie("Option_1",v_name1, max_age=30)
            response.set_cookie("Villager_1",v_img1, max_age=30)
            response.set_cookie("Option_2",v_name2, max_age=30)
            response.set_cookie("Villager_2",v_img2, max_age=30)
            return response
        else:
            
            
            return HttpResponse("Please fill out all questions.")
    # print(request.POST)
    return render(request, 'find_villager/index.html')


def villager_response(request):
    if request.method == 'POST':
        form = VillagerResponse(request.POST)
        
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print(form.cleaned_data)
          
            form_data = VillagerResponseDB(villager_option=form.cleaned_data['villager_option'],
                                           villager_why = form.cleaned_data['villager_why'])
            form_data.save()
         
            return render(request, 'find_villager/thankyou.html')
        
        else:
            
            return HttpResponse("Please fill out all questions.")
    else:
        vi1 = request.COOKIES["Option_1"]
        vim1 = request.COOKIES["Villager_1"]
        vi2 = request.COOKIES["Option_2"]
        vim2 = request.COOKIES["Villager_2"]
    
        return render(request, 'find_villager/results.html', context = {"Option_1":vi1,"Villager_1":vim1,
                                                                    "Option_2":vi2,"Villager_2":vim2})




