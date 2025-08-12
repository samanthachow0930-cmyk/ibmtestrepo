import scrapy
import os
import hashlib
from urllib.parse import urljoin

class USTSpider(scrapy.Spider):
    name = "ust"
    start_urls = [
        "https://facultyprofiles.hkust.edu.hk/facultylisting.php", #domain name
    ]

    def parse(self, response):
        # Get all the cards
        cards = response.css('.results-div')

        # Iterate over the cards
        for card in cards:
            # Get the profile URL for each card
            profile_URL = card.css('a.profile-link::attr(href)').get()
            # Follow the profile URL
            yield response.follow(profile_URL, callback=self.parse_profile, cb_kwargs={'profile_URL': profile_URL})

    def parse_profile(self, response, profile_URL):
        #Get all info about the professor inside the profile page
        print("entered_profile")
        code = hashlib.sha1(profile_URL.url.encode()).hexdigest() #giving a unique code to each profile
        name = response.css("#title-name::text").get() 
        chin_name = response.css('.name-chi::text').get()
        post = response.css('.post::text').get()
        dept = response.css('.post .unit::text').get()
        tel = response.css('li:has(.fa-phone)::text').get()
        room = response.css('li:has(.fa-building) a::attr(href)').get()
        URL = profile_URL
        #personalweb = response.css('li:has(.fa-id-card-alt) a::attr(href)').get()
        research_interest = response.css('a#researchinterestTab ::attr(href)').get()
        publications = response.css('a#publicationsContent ::attr(href)').get()
        projects = response.css('a#rshProjSnap a::text').get()
        imageURL = response.css('.profile-image img::attr(src)').get()
        absolute_imageURL = response.urljoin("https://facultyprofiles.hkust.edu.hk.", imageURL)
        
        yield {
            "code": code,
            "name": name,  
            "chin_name": chin_name,
            "post": post,
            "dept": dept,
            "tel": tel,
            "room": room,
            "URL": URL,
            #"personalweb" : personalweb,
            "research_interest": research_interest,
            "publications": publications,
            "projects": projects,
            "image_urls": absolute_imageURL,
        }
