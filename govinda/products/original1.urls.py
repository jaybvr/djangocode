from django.urls import path
from .views import generatePDF

from . import views

urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('list_main', views.list_main, name='list_main'),
    path('logout', views.logout_user, name='logout_user'),
    path('list_groups', views.list_groups, name='list_groups'),
    path('list_inventory', views.list_inventory, name='list_inventory'),
    path('add_sales', views.add_sales, name='add_sales'),
    path('import_data', views.import_data, name='import_data'),
    path('list_alerts', views.list_alerts, name='list_alerts'),
    path('export_host_list', views.export_host_list, name='export_host_list'),
    path('add_group', views.add_group, name='add_group'),
    path('edit_group', views.edit_group, name='edit_group'),
    path('delete_group', views.delete_group, name='delete_group'),
    path('add_inventory', views.add_inventory, name='add_inventory'),
    path('edit_inventory', views.edit_inventory, name='edit_inventory'),
    path('delete_inventory', views.delete_inventory, name='delete_inventory'),
    path('cart_checkout', views.cart_checkout, name='cart_checkout'),
    path('clear_cart', views.clear_cart, name='clear_cart'),
    path('update_cart', views.update_cart, name='update_cart'),
    path('edit_cart', views.edit_cart, name='edit_cart'),
    path('list_customers', views.list_customers, name='list_customers'),
    path('list_orders', views.list_orders, name='list_orders'),
    path('list_order_items', views.list_order_items, name='list_order_items'),
    path('generatePDF', views.generatePDF, name='generatePDF'),
    path('generatePDF1', views.generatePDF1, name='generatePDF1'),
    path('gen_report', views.gen_report, name='gen_report'),
    path('list_bu', views.list_bu, name='list_bu'),
    path('add_bu', views.add_bu, name='add_bu'),
    path('edit_bu', views.edit_bu, name='edit_bu'),
    path('delete_bu', views.delete_bu, name='delete_bu'),
    path('ajax/load-groups/', views.load_groups, name='ajax_load_groups'),
    path('load_groups', views.load_groups, name='load_groups'),
    path('list_alerts', views.list_alerts, name='list_alerts'),
    path('gen_summary_repo', views.gen_summary_repo, name='gen_summary_repo'),
    path('gen_alert_repo', views.gen_alert_repo, name='gen_alert_repo'),
    path('gen_summary', views.gen_summary, name='gen_summary'),
    path('edit_customer', views.edit_customer, name='edit_customer'),
    path('delete_customer', views.delete_customer, name='delete_customer'),

    path('get_inventory', views.get_inventory, name='get_inventory'),


    




]