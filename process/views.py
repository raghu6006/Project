from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from .models import PhoneStore, EmailStore, Contact, Group
import json

# Create your views here.      

def getIds(email, phone_number):
    email_id = -2
    phone_number_id = -2
    if len(email)>0:
        email_instances = EmailStore.objects.filter(email=email)
        if email_instances.exists():
            email_id = email_instances[0].pk
        else:
            email_id = -1
        
    if len(phone_number)>0:
        phone_num_instance = PhoneStore.objects.filter(number=phone_number)
        if phone_num_instance.exists():
            phone_number_id  = phone_num_instance[0].pk
        else:
            phone_number_id = -1


    return email_id, phone_number_id

def getContacts( email, phone_number):
    email_id, phone_number_id = getIds(email, phone_number)
    #primary_contacts = set(Contact.objects.filter(main_query & primary_query))
    #sec_contacts = set(Contact.objects.filter(main_query & sec_query))

    curr_email = None
    if email_id ==-1:
        curr_email = EmailStore(email=email)
        curr_email.save()
    elif email_id>0:
        curr_email = EmailStore.objects.get(email=email)
    curr_phone = None
    if phone_number_id == -1:
        curr_phone = PhoneStore(number=phone_number)
        curr_phone.save()
    elif phone_number_id>0:
        curr_phone = PhoneStore.objects.get(number=phone_number)
    
    new_contact = Contact(phoneNumber=curr_phone, email=curr_email, linkPrecedence = Contact.primary,
                          createdAt = timezone.now() )
    new_contact.save()
    new_group  = Group(number=new_contact.id, contact=new_contact)
    new_group.save()
    #primary_contacts.append(new_contact)
    
    email_id, phone_number_id = getIds(email, phone_number)
    main_query = Q(email__id=email_id) | Q(phoneNumber__id=phone_number_id)
    primary_query = Q(linkPrecedence = Contact.primary)
    sec_query = Q(linkPrecedence = Contact.sec)

    contacts =  Contact.objects.filter(main_query).distinct()
    group_numbers = Group.objects.filter(contact__in = contacts).values_list('number', flat=True).distinct()

    #primary_contacts = Group.objects.filter(number=group_numbers).values_list("contact", True)
    contacts = Contact.objects.filter(groups__number__in=group_numbers)
    primary_contacts = contacts.filter(primary_query)
    sec_contacts = contacts.filter(sec_query)

    #primary_contacts = Contact.objects.filter(main_query & primary_query).distinct()
    #sec_contacts = Contact.objects.filter(main_query & sec_query).distinct()
    return primary_contacts, sec_contacts

def process(primary_contacts, sec_contacts):
    primary = primary_contacts[0]
    all_emails = set()
    all_numbers = set()
    sec_ids = []
    for contact in primary_contacts:
        if contact.createdAt<primary.createdAt:
            primary = contact

    for contact in primary_contacts.union(sec_contacts):
        contact.linkedId = primary.id
        contact.linkPrecedence = Contact.sec
        contact.updatedAt = timezone.now()
        contact.save()
        for group in contact.groups.all():
            group.number=primary.id
            group.save()
        if contact.email:
            all_emails.add(contact.email.email)
        if contact.phoneNumber:
            all_numbers.add(contact.phoneNumber.number)
        sec_ids.append(contact.id)

    primary.linkedId = None
    primary.linkPrecedence = Contact.primary
    primary.updatedAt = timezone.now()
    primary.save()
    sec_ids.remove(primary.id)
    return primary.id, all_emails, all_numbers, sec_ids

def serialisedata(primary_id=None,emails=[],numbers=[],sec_ids=[]):
    data = {
            "contact":
                    {
                    "primaryContatctId":primary_id,
                    "emails":list(emails),
                    "phoneNumbers":list(numbers),
                    "secondaryContactIds":sec_ids
                    }
            }
    serialised_data = json.dumps(data, indent=4)
    return serialised_data


class IndexView(APIView):
    def post(self, request):
        data = request.data
        email = data["email"].replace(" ","")
        phone_number = data["phoneNumber"].replace(" ","")

        if len(phone_number)+len(email)==0:
            return Response(200)
        primary_contacts, sec_contacts = getContacts(email, phone_number)
        primary_id, emails, numbers, sec_ids = process(primary_contacts, sec_contacts)

        return Response(serialisedata(primary_id, emails, numbers, sec_ids))
    
    def get(self, request):
        return Response(200)
    

@csrf_exempt
def index(request):
    if request.method == "POST":
        payload = json.loads(request.body)
        email = payload.get("email").replace(" ","")
        phone_number = payload.get("phoneNumber").replace(" ","")

        if len(phone_number)+len(email)==0:
            return HttpResponse(serialisedata(), content_type = "application/json")
        
        primary_contacts, sec_contacts = getContacts(email, phone_number)
        primary_id, emails, numbers, sec_ids = process(primary_contacts, sec_contacts)

        return HttpResponse(serialisedata(primary_id, emails, numbers, sec_ids), content_type = "application/json")
    
    return HttpResponse("NUll")