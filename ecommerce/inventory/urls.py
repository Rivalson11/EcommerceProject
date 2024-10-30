from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path("products", views.ProductListView.as_view(), name="products"),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("product/add/", views.ProductCreateView.as_view(), name="product_add"),
    path("product/<int:pk>/edit/", views.ProductEditView.as_view(), name="product_edit"),
    path(
        "product/<int:pk>/delete/",
        views.ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path(
        "generate-report/<str:report_type>/",
        views.DownloadReportView.as_view(),
        name="download_report",
    ),
    path(
        "download-report/<str:task_id>/",
        views.CheckTaskStatusView.as_view(),
        name="check_task_status",
    ),
]
