from requests import get, post
from re import findall,search
import  re
from urllib.parse import urlparse, parse_qs
import random,string,os,warnings
from json import loads,dumps
warnings.filterwarnings("ignore")
from .expection import DownloaderError, InvalidURL, DownloadFailed, NetworkError, FileWriteError
from .parsing import get_video_id,headers_fb,YT_cookie_dict,YT_headers,headers_ins
def rand_str(n): return ''.join(random.choices(string.ascii_letters + string.digits + '-_', k=n))

class downloder:
    def __init__(self, url):
        self.url = url
        self.headers=headers_fb
        self.Fyle_type=None
    def __enter__(self):
        # you can do setup here
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        # cleanup (optional)
        pass
    @property
    def platform(self):
        if not self.url.startswith("http"):
            raise InvalidURL("URL must start with http or https")
        if 'youtube.com' in self.url or 'youtu.be' in self.url:
            return 'youtube'
        elif 'facebook.com' in self.url or 'fb.watch' in self.url:
            return 'facebook'
        elif 'instagram' in self.url.lower():
            return 'instagram'
        else:
            raise InvalidURL("Unsupported platform URL")
    def decode_responce(self, responce):
        try:
            return responce.encode('utf-8').decode('unicode_escape').encode('utf-16', 'surrogatepass').decode('utf-16').replace('\\','')
        except Exception as e:
            print(e)
    def facebook_video(self):
        try:
            if self.platform != 'facebook':
                raise InvalidURL("Unsupported platform URL")
            title = None
            response = self.decode_responce(get(self.url, headers=self.headers).text).replace('\\','')
            # open('tempss.txt', 'w' ,encoding= 'utf-8').write(response)
            try:
                browser_native_hd_url= 'https://video'+findall(r'd_url":"https://video(.*?)"', response)[-1]
                output_file = "facebook_video.mp4"
                Fyle_type ="Video"
                title = search(r'"message":{"text":"(.*?)","', str(response))
                if title:
                    title = title.group(1)
            except  Exception as e:
                browser_native_hd_url= search(r'"image":{"uri":"(.*?)"', response).group(1)
                output_file = "facebook_photo.jpg"
                Fyle_type ="Image"
                title = search(r'"color_ranges":\[\],"text":"(.*?)"', str(response))
                if title:
                    title = title.group(1)
            return ({'url':self.url,
                          'download_url':browser_native_hd_url.replace('\\','') if browser_native_hd_url else None,
                          'output_file':output_file if browser_native_hd_url else None,
                          'title':title if title else None,
                          'Fyle_type':Fyle_type if Fyle_type else None,
                          'platform':self.platform if self.platform else None,
                          'success': True if browser_native_hd_url else False
                          })
        except Exception as e:
            raise NetworkError(f"Network error: {e}")
    def youtube_video(self,quality=1080):
        
        try:
            json_data = {
                'url': self.url,
            }

            response = post('https://www.clipto.com/api/youtube', cookies=YT_cookie_dict(), headers=YT_headers, json=json_data)
    
            response =response.json()
            print(response['success'])
            if response['success'] == True:
                url= response['url']
                title = response['title']
                medias = response['medias']
                url=response['medias'][0]['url']
                output_file = "youtube_video.mp4"
                Fyle_type ="Video"
                return ({'url':self.url,
                          'download_url':url if url else None,
                          'output_file':output_file if url else None,
                          'title':title if title else None,
                          'Fyle_type':Fyle_type if Fyle_type else None,
                          'platform':self.platform if self.platform else None,
                          'success': True if url else False
                          })
         
            # # print(get_video_id(self.url))
            # if self.platform != 'youtube':
            #     raise InvalidURL("Unsupported platform URL")
            # video_id= get_video_id(self.url)
            # print(video_id)
            # if quality ==0:
            #     return {"url":self.url,"download_url": None, "output_file": None,"success": False}
            # if  video_id:
            #     json_data = {
            #         'videoId': video_id,
            #         'quality': str(quality),
            #     }
            #     response = (post('https://dlsrv.online/api/download/mp4', headers=headers_yt, json=json_data).text)
            #     # print(response)
            #     try:
            #         html = loads(response)["modalHtml"]
            #     except Exception as e:
            #         self.youtube_video(quality-360)
            #     pattern = r"https://yt1s-worker-\d+\.dlsrv\.online/tunnel\?[^'\" ]+"
            #     match = search(pattern, html)
            #     if match:
            #         extracted_url = match.group(0)
            #         return {"url":self.url,"download_url": extracted_url, "output_file": f"{video_id}.mp4" if extracted_url else None,"success": True}
            #     else:
            #         return {"url":self.url,"download_url": None, "output_file": None,"success": False}
        except Exception as e:
            
            raise NetworkError(f"Network error: {e}")
    def instagram_video(self):
        try:
            if self.platform != 'instagram':
                raise InvalidURL("Unsupported platform URL")
            captio=None
            d_url=None
            get_req=self.decode_responce(get(self.url, headers=headers_ins).text)
            # open('tempss.txt', 'w', encoding='utf-8').write(get_req)

            pattern = re.compile(r'"video_versions":\[\{"width":(.*?),"height":(.*?),"url":"(.*?)"')
            match = search(pattern, get_req)
            pattern = re.compile(r',"caption":\{"text":"(.*?)"', re.DOTALL)
            match_2 = search(pattern, get_req)
            if match:
                d_url = match.group(3)
                if match_2:
                    captio=match_2.group(1)
            return  {"url":self.url,"download_url": d_url, "output_file": f"video_.mp4" if d_url else None,"success": True if d_url else None,"captio":captio }
        except Exception as e:
            raise NetworkError(f"Network error: {e}")
    def save_file(self, url, output_file='output_file.mp4'):
        try:
            if not url.startswith("http"):
                raise InvalidURL("URL must start with http or https")
            response = get(url, stream=True)
            # filepath = os.path.join('videos', 'output_file.mp4')
            # Try to get total size
            total_size = response.headers.get('content-length')
            if total_size is None:
                total_size = 0
            else:
                total_size = int(total_size)
            downloaded = 0
            if response.status_code == 200:
                with open(output_file, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total_size > 0:
                                # Show percent when total size is known
                                percent = (downloaded / total_size) * 100
                                print(f"\rDownloading: {percent:.2f}% ", end="")
                            else:
                                # Show MB downloaded when total unknown
                                mb = downloaded / (1024 * 1024)
                                print(f"\rDownloading: {mb:.2f} MB ", end="")
                print("\n✅ Download complete:", output_file)
                return output_file
            else:
                print("❌ Download failed!")
                raise DownloadFailed("Download failed with status code:", response.status_code)
        except Exception as e:
            raise NetworkError(f"Network error: {e}")
    def download(self, output_file=None):
        output_file = output_file if output_file else info['output_file']
        if not self.url.startswith("http"):
            raise InvalidURL("URL must start with http or https")
        if 'facebook' in self.platform:
            info=self.facebook_video()
            if info['success']:
                return self.save_file(info['download_url'], output_file= output_file)
        elif 'youtube' in self.platform:
            info= self.youtube_video()
            if info['success']:
                return self.save_file(info['download_url'], output_file= output_file)
        elif 'instagram' in self.platform:
            infp=self.instagram_video()
            if infp['success']:
                return self.save_file(infp['download_url'], output_file=output_file)
        else:
            raise InvalidURL("Unsupported platform URL")
# x=downloads('https://www.youtube.com/watch?v=hYZKrPOyEYk')
# dolon=x.youtube_video()
# print(dolon)
# # x.save_file(str(dolon['download_url']), output_file=f'downloads/{dolon['output_file']}')
# with downloder('https://www.youtube.com/watch?v=o0eAWXs19jE&list=RDo0eAWXs19jE&start_radio=1') as x:
#     print(x.download(output_file='videos/output_instas.mp4'))
