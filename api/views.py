from rest_framework import generics
from ytmusicapi import YTMusic
from rest_framework import status
from django.http import JsonResponse
from pytube import YouTube   
from rest_framework.decorators import api_view
from rest_framework.response import Response
import sys
import json




# class SearchAPIView(generics.CreateAPIView):
    
#     def create(self, request, *args, **kwargs):
#         query = request.data.get('query')
#         if query:
#             ytmusic = YTMusic()
#             result = ytmusic.search(query)
#             return Response({'query': query, 'result': result}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'error': 'Search query is required'}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

class SearchResultSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=255)
    result = serializers.JSONField()

    def create(self, validated_data):
        return SearchResult.objects.create(**validated_data)

class SearchAPIView(APIView):
    serializer_class = SearchResultSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data['query']
            ytmusic = YTMusic()
            result = ytmusic.search(query)
            serializer.validated_data['result'] = result
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








def get_audio_url(video_id):
    yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
    audio_stream = yt.streams.filter(only_audio=True).first()
    return audio_stream.url

def play_audio(request):
    video_id = request.GET.get('video_id')
    if not video_id:
        return JsonResponse({'error': 'No video ID provided'}, status=400)

    audio_url = get_audio_url(video_id)
    return JsonResponse({'audio_url': audio_url})






# Set the default encoding to UTF-8 to avoid encoding errors
sys.stdout.reconfigure(encoding='utf-8')
@api_view(['GET'])
def get_chart_data(request):
    ytmusic = YTMusic()

    # Fetching the chart data for global (ZZ)
    chart_data = ytmusic.get_charts('ZZ')

    # List to store video data
    video_list = []

    # Iterate through the video items and append details to the list
    for item in chart_data['videos']['items']:
        title = item['title']
        videoId = item['videoId']
        thumbnails = item.get('thumbnails', [])
        thumbnail_url = thumbnails[0]['url'] if thumbnails else 'N/A'
        artists = item.get('artists', [])
        artist_names = ', '.join([artist['name'] for artist in artists])

        # Encode the title and videoId to UTF-8
        title_utf8 = title.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
        videoId_utf8 = str(videoId).encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
        artist_names_utf8 = artist_names.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)




        # Create a dictionary for the current video item and append it to the list
        video_data = {
            "title": title_utf8,
            "videoId": videoId_utf8,
            "thumbnail_url": thumbnail_url,
            "artists": artist_names_utf8
        }
        video_list.append(video_data)

    # Convert the list to JSON format
    video_json = json.dumps(video_list, ensure_ascii=False)
    data_list = json.loads(video_json)



    # Convert the list to a dictionary
    data_dict = {}
    for i, item in enumerate(data_list):
        data_dict[str(i)] = item

    # Convert the dictionary to JSON
    json_data = json.dumps(data_dict, ensure_ascii=False)

    Real_Data = json.loads(json_data)

    # Return the JSON response
    return Response(Real_Data)






def get_audio_download(video_id):
    yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download("media/music", "audio.mp3")

def download_audio(request):

    try:
        video_id = request.GET.get('video_id')
        if not video_id:
            return JsonResponse({'error': 'No video ID provided'}, status=400)

        get_audio_download(video_id)
        # return JsonResponse({'status': 'success', 'message': 'Audio downloaded successfully'})

        base_audio_url = 'http://localhost:8000/media/music/'

        audio_url = base_audio_url + 'audio.mp3'


        response_data = {
                'status': 'success',
                'message': 'Audio downloaded successfully',
                'audio_url': audio_url
            }
        
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})






    
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus


# URL Path to Link
BASE_URL = 'https://www.pdfdrive.com/search?q={}&pagecount=&pubyear=&searchin=&em='


@method_decorator(csrf_exempt, name='dispatch')
class SearchAPIViewBook(View):
    def get(self, request):
        # Collect Data From Form
        search = request.GET.get('search')

        # If Form Data has space, replace space with '+'
        url = BASE_URL.format(quote_plus(search))

        # Turn URL into HTML Text
        source = requests.get(url).text

        # Create Soup Object
        soup = BeautifulSoup(source, 'lxml')

        # Find Div Tag with Class
        div = soup.find('div', class_="files-new")

        # Create An Empty List
        books = []

        if div:
            for pdf in div.find_all('li'):
                image = pdf.find('img')['src']
                title = pdf.find('img')['title']
                link = pdf.find('a')['href']
                try:
                    page = pdf.find('span', class_="fi-pagecount").text
                except AttributeError:
                    page = 'N/A'
                year = pdf.find('span', class_="fi-year").text
                try:
                    downloads = pdf.find('span', class_="fi-hit").text
                except AttributeError:
                    downloads = 'N/A'

                books.append({
                    'title': title,
                    'image': image,
                    'link': link,
                    'page': page,
                    'year': year,
                    'downloads': downloads
                })

        data = {
            'search': search,
            'books': books,
        }

        return JsonResponse(data)
    



    
from rest_framework.views import APIView
import requests
from bs4 import BeautifulSoup

class PDFDriveInfo(APIView):
    def get(self, request):
        # Get the required_html from the query parameters
        required_html = request.GET.get('required_html')

        if not required_html:
            return Response({"error": "required_html parameter is required"}, status=400)

        # Construct the URL using the required_html
        url = f'https://www.pdfdrive.com/{required_html}'

        # Send a GET request to the webpage
        response = requests.get(url)

        if response.status_code != 200:
            return Response({"error": "Failed to fetch data from the provided URL"}, status=response.status_code)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div with class "ebook-buttons"
        ebook_buttons_div = soup.find('div', class_='ebook-buttons')

        # Initialize variables to store extracted data
        preview_data_id = None
        preview_data_preview = None
        download_href = None

        # Extract relevant data if the div is found
        if ebook_buttons_div:
            # Extract data from the preview button
            preview_button = ebook_buttons_div.find('button', id='previewButtonMain')
            if preview_button:
                preview_data_id = preview_button.get('data-id')
                preview_data_preview = preview_button.get('data-preview')

            # Extract data from the download link
            download_link = ebook_buttons_div.find('a', id='download-button-link')
            if download_link:
                download_href = download_link.get('href')

        # Construct the response data
        response_data = {
            "preview_data_id": preview_data_id,
            "preview_data_preview": preview_data_preview,
            "download_href": download_href
        }

        return Response(response_data)






    
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import io
from django.http import FileResponse, HttpResponse

def download_pdf(request):
    # Get the required_html and pdf_name from the query parameters
    required_html = request.GET.get('required_html')
    pdf_name = request.GET.get('pdf_name')

    if not required_html:
        return JsonResponse({"error": "required_html parameter is required"}, status=400)

    if not pdf_name:
        return JsonResponse({"error": "pdf_name parameter is required"}, status=400)

    # Construct the URL using the required_html
    url = f'https://www.pdfdrive.com/{required_html}'

    # Configure Chrome options for running the browser in the background
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run the browser in background

    # Create a new instance of the Chrome driver with configured options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Set the maximum waiting time
        driver.implicitly_wait(5)

        # Open the webpage
        driver.get(url)

        # Find the <a> tag containing the download link
        download_link = driver.find_element(By.CSS_SELECTOR, 'a.btn-primary')

        # Extract the href attribute value
        if download_link:
            download_url = download_link.get_attribute('href')

            # Close the browser
            driver.quit()

            # Send a GET request to the download URL to initiate the download
            response = requests.get(download_url)

            if response.status_code == 200:
                # Return the PDF file as a FileResponse with the specified filename
                pdf_file = response.content
                return FileResponse(io.BytesIO(pdf_file), as_attachment=True, filename=f'{pdf_name}.pdf')
            else:
                return HttpResponse("Failed to initiate PDF download.", status=500)
        else:
            return HttpResponse("Failed to initiate PDF download.", status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)})
    finally:
        # Close the browser
        driver.quit()




# views.py
def extract_data_from_webpage(request):
    required_html = request.GET.get('required_html')

    if not required_html:
        return JsonResponse({"error": "required_html parameter is required"}, status=400)

    url = f'https://www.pdfdrive.com/{required_html}'

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        ebook_buttons_div = soup.find('div', class_='ebook-buttons')

        if ebook_buttons_div:
            preview_button = ebook_buttons_div.find('button', id='previewButtonMain')
            if preview_button:
                preview_data_preview = preview_button.get('data-preview')
                view_url = f'https://www.pdfdrive.com{preview_data_preview}'
                return JsonResponse({"view_url": view_url})
        else:
            return JsonResponse({"error": "ebook-buttons div not found."}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
