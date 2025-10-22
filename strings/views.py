from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from .models import StoredString
from .serializers import CreateStringSerializer, StoredStringSerializer
from .utils import compute_properties, sha256_of, parse_nl_query
from django.db.models import Q
import json

MAX_LENGTH = 10000  # set a safety limit for incoming strings

class CreateStringView(APIView):
    def get(self, request):
        """List strings with filters (delegates to ListStringsView)"""
        return ListStringsView().get(request)

    def post(self, request):
        ser = CreateStringSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        value = ser.validated_data['value']
        if not isinstance(value, str):
            return Response({"detail": "\"value\" must be a string"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if len(value) > MAX_LENGTH:
            return Response({"detail": "String too long"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        props = compute_properties(value)
        sid = props['sha256_hash']
        if StoredString.objects.filter(Q(id=sid) | Q(value=value)).exists():
            return Response({"detail": "String already exists"}, status=status.HTTP_409_CONFLICT)
        obj = StoredString.objects.create(id=sid, value=value, properties_json=props)
        return Response(obj.as_dict(), status=status.HTTP_201_CREATED)

class StringDetailView(APIView):
    def get(self, request, string_value):
        obj = StoredString.objects.filter(value=string_value).first()
        if not obj:
            sid = sha256_of(string_value)
            obj = StoredString.objects.filter(id=sid).first()
        if not obj:
            return Response({"detail": "String not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(obj.as_dict(), status=status.HTTP_200_OK)

    def delete(self, request, string_value):
        obj = StoredString.objects.filter(value=string_value).first()
        if not obj:
            sid = sha256_of(string_value)
            obj = StoredString.objects.filter(id=sid).first()
        if not obj:
            return Response({"detail": "String not found"}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ListStringsView(APIView):
    def get(self, request):
        # parse query params
        is_palindrome = request.query_params.get('is_palindrome')
        min_length = request.query_params.get('min_length')
        max_length = request.query_params.get('max_length')
        word_count = request.query_params.get('word_count')
        contains_character = request.query_params.get('contains_character')

        # validate types
        try:
            if is_palindrome is not None:
                if is_palindrome.lower() not in ['true', 'false']:
                    raise ValueError("is_palindrome must be true/false")
                is_palindrome = is_palindrome.lower() == 'true'
            if min_length is not None:
                min_length = int(min_length)
            if max_length is not None:
                max_length = int(max_length)
            if word_count is not None:
                word_count = int(word_count)
            if contains_character is not None:
                if len(contains_character) != 1:
                    raise ValueError("contains_character must be a single character")
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        qs = StoredString.objects.all()
        results = []
        for obj in qs:
            props = obj.properties_json
            ok = True
            if is_palindrome is not None and props.get('is_palindrome') != is_palindrome:
                ok = False
            if min_length is not None and props.get('length', 0) < min_length:
                ok = False
            if max_length is not None and props.get('length', 0) > max_length:
                ok = False
            if word_count is not None and props.get('word_count') != word_count:
                ok = False
            if contains_character is not None and contains_character not in obj.value:
                ok = False
            if ok:
                results.append(obj.as_dict())

        filters_applied = {}
        if is_palindrome is not None: filters_applied['is_palindrome'] = is_palindrome
        if min_length is not None: filters_applied['min_length'] = min_length
        if max_length is not None: filters_applied['max_length'] = max_length
        if word_count is not None: filters_applied['word_count'] = word_count
        if contains_character is not None: filters_applied['contains_character'] = contains_character

        return Response({"data": results, "count": len(results), "filters_applied": filters_applied})

class FilterByNaturalLanguageView(APIView):
    def get(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response({"detail": "query param required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            parsed = parse_nl_query(query)
        except ValueError:
            return Response({"detail": "Unable to parse natural language query"}, status=status.HTTP_400_BAD_REQUEST)

        # check obvious conflicts (example pattern)
        if 'min_length' in parsed and 'max_length' in parsed and parsed['min_length'] > parsed['max_length']:
            return Response({"detail": "Conflicting filters"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # re-use ListStringsView logic by building a fake request-like param dict
        # We'll just filter here:
        qs = StoredString.objects.all()
        results = []
        for obj in qs:
            props = obj.properties_json
            ok = True
            if parsed.get('is_palindrome') is not None and props.get('is_palindrome') != parsed.get('is_palindrome'):
                ok = False
            if parsed.get('min_length') is not None and props.get('length', 0) < parsed.get('min_length'):
                ok = False
            if parsed.get('max_length') is not None and props.get('length', 0) > parsed.get('max_length'):
                ok = False
            if parsed.get('word_count') is not None and props.get('word_count') != parsed.get('word_count'):
                ok = False
            if parsed.get('contains_character') is not None and parsed.get('contains_character') not in obj.value:
                ok = False
            if ok:
                results.append(obj.as_dict())

        return Response({
            "data": results,
            "count": len(results),
            "interpreted_query": {
                "original": query,
                "parsed_filters": parsed
            }
        })

