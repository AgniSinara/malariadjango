from django.shortcuts import render, redirect
from .ml.ml_model import model_predict
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.conf import settings
import os
import numpy as np

# Create your views here.


def index(request):
    return render(request, 'index.html')


def predict(request):
    if request.method == 'POST':
        f = request.FILES['image']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            settings.MEDIA_ROOT, 'uploads', f.name)
        # f.save(file_path)

        print(file_path)

        file_name = default_storage.save(file_path, f)

        # Make prediction
        preds = model_predict(file_path)
        classes = ['Parasitized', 'Uninfected']

        # Process your result for human
        # preds = np.argmax(preds, axis=1)            # Simple argmax
        # pred_class = decode_predictions(preds, top=1)   # ImageNet Decode
        result = str('{}'.format(classes[np.argmax(preds[0])]))  # Convert to string
        print(result)
        return HttpResponse(result)

