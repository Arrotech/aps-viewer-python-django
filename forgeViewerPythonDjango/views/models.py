from cgi import print_form
from django.shortcuts import render
from dotenv import load_dotenv
import os
from ..services.oss import list_objects, upload_object
from ..services.md import get_manifest, translate_object
from autodesk_forge_sdk.md import urnify
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

load_dotenv()


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def upload_obj(request):
    try:
        if request.method == 'GET':
            objects = list_objects(bucket_key=os.getenv("FORGE_BUCKET"))
            return JsonResponse(objects, safe=False)
        elif request.method == 'POST':
            if 'model-file' in request.FILES:
                filedata = request.FILES['model-file']
                if filedata.name != '':
                    if filedata:
                        f = filedata.read()
                        buff = bytearray(f)
                        filename = filedata.name
                        uploaded_model = upload_object(bucket_key=os.getenv(
                            "FORGE_BUCKET"), filename=filename, buff=buff)
                        translate_object(urnify(uploaded_model["objectId"]), [
                            {"type": "svf", "views": ["2d", "3d"]}])
                        return JsonResponse({"name": uploaded_model["objectKey"],
                                             "urn": urnify(uploaded_model["objectId"])},
                                            safe=False)
                    return JsonResponse({"error": "No file selected"})
                return JsonResponse({"error": "No file selected"})
            return JsonResponse({"error": "No file uploaded"})
    except Exception as e:
        return JsonResponse({"error": str(e)})


def get_status(request, urn):
    try:
        manifest = get_manifest(urn)
        if manifest:
            messages = []
            if manifest["derivatives"]:
                for derivative in manifest["derivatives"]:
                    messages.extend(
                        derivative["messages"] if "messages" in derivative else [])
            return JsonResponse({"status": manifest["status"], "progress": manifest["progess"], "messages": messages})
        else:
            return JsonResponse({"status": "n/a"})
    except Exception as e:
        return JsonResponse({"error": str(e)})
