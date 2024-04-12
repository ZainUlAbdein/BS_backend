from django.urls import path
from .views import AudioAPIView, PDFDriveInfo,  SearchAPIView, SearchAPIViewBook, download_pdf, extract_data_from_webpage,  get_chart_data
from . import views




urlpatterns = [
    path('search/', SearchAPIView.as_view(), name='search'),
    path('play_audio/', views.play_audio, name='play_audio'),
    path('chart-data/', get_chart_data, name='chart_data'),
    path('audio/<str:video_id>/', AudioAPIView.as_view(), name='audio-api'),
    path('BookSearch/', SearchAPIViewBook.as_view(), name='Book_search_api'),
    path('pdf-drive-info/', PDFDriveInfo.as_view(), name='pdf_drive_info'),
    path('download-pdf/', download_pdf, name='download_pdf'),
    path('extract-data/', extract_data_from_webpage, name='extract_data'),


]
