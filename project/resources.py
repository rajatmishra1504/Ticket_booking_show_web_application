from flask_restful import Api, Resource, reqparse
from model import *

api = Api()


parser = reqparse.RequestParser()









class Api_admins(Resource):
    def get(self):

        all_admins = {}

        a1 = Admin.query.all()

        for admin in a1:
            all_admins[admin.id] = admin.username

        return all_admins

class Api_users(Resource):
    def get(self):

        all_users = {}
        u1 = User.query.all()
        for user in u1:
            all_users[user.id] = user.username
        return all_users

class Api_venues(Resource):



    def get(self):
        all_venues = {}
        v1 = Venue.query.all()

        for ven in v1:
            all_venues[ven.v_id] = {"venue_name" : ven.v_name, "venue_location" : ven.v_location, "venue_capacity" : ven.v_capacity, "current_no._f_shows" : len(ven.v_shows), "current_no._of_bookings": len(ven.bookings)}
        return all_venues

    def put(self,id):

        parser.add_argument("venue_name", required=True)
        parser.add_argument("venue_location", required=True)
        parser.add_argument("venue_capacity", required=True)
        info = parser.parse_args()
        v = Venue.query.get(id)
        v.v_name = info["venue_name"]
        v.v_location = info["venue_location"]
        v.v_capacity = info["venue_capacity"]
        db.session.commit()

        return {"venue_name" : v.v_name, "venue_location" : v.v_location, "venue_capacity" : v.v_capacity, "current_no._f_shows" : len(v.v_shows), "current_no._of_bookings": len(v.bookings) , "status": "updated"} 

    def post(self, a_id):

        parser.add_argument("venue_name", required=True)
        parser.add_argument("venue_location", required=True)
        parser.add_argument("venue_capacity", required=True)


        info = parser.parse_args()

        v = Venue.query.filter_by(v_name = info["venue_name"], v_location = info["venue_location"]).first()
        if v:
            return {"message" : "Venue already exists with this name and at this location"}, 400

        

        db.session.add(Venue(v_name = info["venue_name"], v_location = info["venue_location"], v_capacity = info["venue_capacity"], v_admin_id = a_id))
        
        db.session.commit()
        new_venue = {"venue_name" : info["venue_name"],"venue_location" : info["venue_location"],"venue_capacity" : info["venue_capacity"], "venue_admin_id" : a_id}
        return new_venue, 201

    def delete(self, v_id):
        v = Venue.query.get(v_id)
        db.session.delete(v)
        db.session.commit()

        return {"status":"Deleted"}, 202

    

class Api_shows(Resource):
    def get(self):
        all_shows = {}
        s1 = Show.query.all()

        
        for s in s1:
            #shiw_list = []
            #for venue in s.venues:
            #venue_dict = {"venue_id": venue.v_id, "venue_name": venue.v_name, "venue_location" : venue.v_location}
            #venue_list.append(venue_dict)
            all_shows[s.s_id] = {"show_name": s.s_name, "show_rating" : s.s_rating, "show_timing" : s.s_timing, "show_price" : s.s_price, "show_director" : s.s_director, "show_capacity" : s.s_capacity, "show_available_seats" : s.s_available_seats, "No.of bookings" : len(s.bookings)}#, "All_venues":venue_list}
        return all_shows
    def post(self, a_id, v_id):

        parser.add_argument("show_name", required=True)
        parser.add_argument("show_rating", required=True)
        parser.add_argument("show_timing", required=True)
        parser.add_argument("show_tag", required=True)
        parser.add_argument("show_price", required=True)
        parser.add_argument("show_director", required=True)
        parser.add_argument("show_capacity", required=True)
        parser.add_argument("show_available_seats", required=True)

        info = parser.parse_args()
        
        v = Venue.query.get(v_id)
        v_s = v.v_shows

        if int(info["show_capacity"]) <= int(0) or int(info["show_available_seats"])<= int(0):
            return {"message":"please Enter Valid Credentials"}, 400
        elif int(info["show_available_seats"]) > int(info["show_capacity"]):
            return {"message":"please Enter Valid Credentials, available seats can't be greater than capacity"}, 400
        else:
            s = Show.query.filter_by(s_name = info["show_name"]).first()
            
            if s:
                if s in v_s:
                    if s.s_timing == info["show_timing"]:
                        return {"message":"This show is already screening at this venue and  at this time"}, 400
                    else:
                        s1 = Show(s_name = info["show_name"], s_rating = info["show_rating"], s_timing = info["show_timing"], s_tags = info["show_tag"], s_price = info["show_price"], s_director = info["show_director"], s_capacity = info["show_capacity"], s_available_seats = info["show_available_seats"], s_admin_id = a_id)
                        db.session.add(s1)
                        v_s.append(s1)
                        db.session.commit()
                        return {"show_name": info["show_name"], "show_rating" : info["show_rating"], "show_timing" : info["show_timing"], "show_tags" : info["show_tag"], "show_price" : info["show_price"], "show_director" : info["show_director"], "show_capacity" : info["show_capacity"], "show_available_seats" : info["show_available_seats"], "show_admin_id" : a_id}, 202
                else:
                    s1 = Show(s_name = info["show_name"], s_rating = info["show_rating"], s_timing = info["show_timing"], s_tags = info["show_tag"], s_price = info["show_price"], s_director = info["show_director"], s_capacity = info["show_capacity"], s_available_seats = info["show_available_seats"], s_admin_id = a_id)
                    db.session.add(s1)
                    v_s.append(s1)
                    db.session.commit()
                    return {"show_name": info["show_name"], "show_rating" : info["show_rating"], "show_timing" : info["show_timing"], "show_tags" : info["show_tag"], "show_price" : info["show_price"], "show_director" : info["show_director"], "show_capacity" : info["show_capacity"], "show_available_seats" : info["show_available_seats"], "show_admin_id" : a_id}, 202
            else:
                s1 = Show(s_name = info["show_name"], s_rating = info["show_rating"], s_timing = info["show_timing"], s_tags = info["show_tag"], s_price = info["show_price"], s_director = info["show_director"], s_capacity = info["show_capacity"], s_available_seats = info["show_available_seats"], s_admin_id = a_id)
                db.session.add(s1)
                v_s.append(s1)
                db.session.commit()
                return {"show_name": info["show_name"], "show_rating" : info["show_rating"], "show_timing" : info["show_timing"], "show_tags" : info["show_tag"], "show_price" : info["show_price"], "show_director" : info["show_director"], "show_capacity" : info["show_capacity"], "show_available_seats" : info["show_available_seats"], "show_admin_id" : a_id}, 202


    def put(self,a_id,v_id,s_id):


        parser.add_argument("show_name", required=True)
        parser.add_argument("show_timing", required=True)
        parser.add_argument("show_tag", required=True)
        parser.add_argument("show_price", required=True)
        parser.add_argument("show_director", required=True)

        info = parser.parse_args()

        a = Admin.query.get(a_id)
        v = Venue.query.get(v_id)
        s = Show.query.get(s_id)

        
        s.s_name = info["show_name"]
        s.s_timing = info["show_timing"]
        s.s_price = info["show_price"]
        s.s_director = info["show_director"]
        db.session.commit()
        return {"show_name": info["show_name"], "show_rating" : s.s_rating , "show_timing" : info["show_timing"], "show_tags" : info["show_tag"], "show_price" : info["show_price"], "show_director" : info["show_director"], "show_capacity" : s.s_capacity, "show_available_seats" : s.s_available_seats, "show_admin_id" : a_id}, 202

    def delete(self,s_id):
        s = Show.query.get(s_id)
        db.session.delete(s)
        db.session.commit()
        return {"message": "Deleted"}, 202
 


api.add_resource(Api_admins, "/api/all_admins")
api.add_resource(Api_users, "/api/all_users")
api.add_resource(Api_venues, "/api/all_venue_details","/api/update_venues/<int:id>","/api/add_venue/<int:a_id>","/api/delete_venue/<int:v_id>")
api.add_resource(Api_shows, "/api/all_shows_details","/api/add_show/<int:a_id>/<int:v_id>","/api/update_show/<int:a_id>/<int:v_id>/<int:s_id>","/api/delete_show/<int:s_id>")

