from django.conf.urls import include, url
from django.contrib import admin
from Testing import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'ToppersNotes.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^create_test/$', views.create_test_backup),
    url(r'^create_class/$', views.create_class),
    url(r'^add_students_in_class/$', views.add_students_in_class),
    url(r'^get_user_classes/$', views.get_user_classes),
    url(r'^send_mail_to_class/$', views.send_mail_to_class),
    url(r'^get_test/$', views.get_test),
    url(r'^$', views.get_home),
    url(r'^start_test/solve$',views.test_view),
    url(r'^dashboard/$', views.get_dashboard),
    url(r'^start_test/$',views.start_test),
    url(r'^test_create/$',views.test_create),
    url(r'^register/$',views.register_user),
    url(r'^login/$',views.login_user),
    url(r'^user_profile/$',views.get_user_info),
    #url(r'^get_all_tests/$',views.get_all_tests),
    url(r'^get_all_tests/$',views.get_all_tests_classwise),
    url(r'^get_user_solved_tests/$',views.get_user_solved_tests),
    url(r'^testwise_students_info/$',views.testwise_students_info),
    url(r'^student_score/$',views.get_all_students_score),
    url(r'^save_test_id/$',views.save_test_id),
    url(r'^clear_test_id/$',views.clear_test_id),
    url(r'^donut_graph_view/$',views.donut_graph_view),
    url(r'^per_question_time_taken/$',views.per_question_time_taken),
    url(r'^per_question_time_taken_topper/$',views.per_question_time_taken_topper),
    url(r'^test_summary_students_rank/$',views.test_summary_students_rank),
    url(r'^overall_percentage/$',views.overall_percentage),
    url(r'^basic_user_test_stats/$',views.basic_user_test_stats),
    url(r'^get_analytics/$',views.get_test_analytics),
    url(r'^add_studnet/$',views.add_student),
    url(r'^get_result/$', views.compute_results)
]
