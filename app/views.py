from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

# new imports
import threading
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

from .serializer import BookSerializer
from django.db import transaction


# Create your views here.


class UploadViewSet(viewsets.ViewSet):

    # ensure atomic transaction
    @transaction.atomic
    def upload(self, request):

        """entry method that handles the upload request"""

        try:
            logger.debug("Upload request received ...")

            request_file = request.data.get("books")

            if request_file:
                logger.debug("File Detected")
            else:
                return Response(
                    {"response": "No file received"}, status=status.HTTP_400_BAD_REQUEST
                )

            # read request file using the appropriate
            # pandas method based on file extension check

            if "xls" in str(request_file).split(".")[-1]:
                file_obj = pd.read_excel(request_file)
            elif "csv" in str(request_file).split(".")[-1]:
                file_obj = pd.read_csv(request_file)
            else:
                return Response(
                    {"response": "Invalid File Format"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # convert file obj to a dataframe,
            # handle empty rows and
            # convert the dataframe to a list of dictionaries

            books_df = pd.DataFrame(file_obj)
            books_df = books_df.replace(np.nan, "", regex=True)
            books = books_df.to_dict(orient="records")

            # instantiate and start thread with required params
            t = threading.Thread(target=self.execute_upload, args=[books], daemon=True)
            t.start()

            return Response(
                {"response": "Upload Initiated, Check Book Table"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.error(f"Error Uploading File. Cause: {str(e)}")
            return Response(
                {
                    "response": f"""Error Uploading File. 
                                             Cause: {str(e)}"""
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def execute_upload(self, books):

        """
        the method that executes the book data upload
        :param books - dict
        """

        try:
            logger.debug("Within the execute_upload() method")

            for book in books:
                try:
                    # serialize and save book data
                    serializer = BookSerializer(data=book)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                    logger.debug(
                        f"Successfully inserted {book['title']}"
                    )
                except Exception as e:
                    logger.error(f"Error Inserting Book. Cause: {str(e)}")
        except Exception as e:
            logger.error(f"Error During Upload. Cause: {str(e)}")
