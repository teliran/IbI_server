## app to server:
POSTs use Body, GETs use Payload

#### app -> server:

| Method        | URL         | Body (json) example  					                    | Description                                                                      | Response example
| ------------- |:------------| -----: 							  			                    | ---: 		                                                                       | ---: 
|GET            | /healthcheck 	  |     | server connactivity                                                   	   | "server alive"
|POST           | /users 	  | {"userId": "9774d56d682e549c", "age": "17", "gender": "male", "timestamp": "dd-MM-yyyy HH:mm:ss"}    | add new user to server                                                    	   | "User added"
|POST           | /actions    | {"userId": "9774d56d682e549c", "sessionId": "001", "timestamp": "dd-MM-yyyy HH:mm:ss", "total_screens": "2", "screen_order": "1", "time_to_pass": "ss", "success": false, "selected_images": "[p1, p7, p22]", "shown_images": "[p1, p5, p7, p19, p22, p46]", "top_rated_images": "[p1, p5, p46]"}	| register an action on server                                                        | "Action registered"
|POST           | /ratings    | {"userId": "9774d56d682e549c", "imageId": "p1", "rating": "6"}                            	                | add rating of image per user                                               | "Rating added"
