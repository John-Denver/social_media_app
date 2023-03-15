from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.urls import resolve, reverse


from post.models import Post, Follow, Stream

