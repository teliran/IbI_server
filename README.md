## app to server:
POSTs use Body, GETs use Payload

#### app -> server:

| Method        | URL         | Body (json) example  					                    | Description                                                                      | Response example
| ------------- |:------------| -----: 							  			                    | ---: 		                                                                       | ---: 
|GET           | /healthcheck 	  |     | server connactivity                                                   	   | "server alive"
|POST           | /user 	  | {"userId": 9774d56d682e549c, "age": "17", "gender": "male", "timestamp": "dd-MM-yyyy HH:mm:ss"}    | add new user to server                                                    	   | "User added"
|POST           | /actions    | {"userId": 9774d56d682e549c, "timestamp": "dd-MM-yyyy HH:mm:ss", "numLockScreens": "2", "success": "0", "timeToEnter": "ss", "metadata": "{}"}	| register an action on server                                                        | "Action registered"
|POST           | /ratings    | {"userId": 9774d56d682e549c, "imageId": "p1", "rating": "6" }                             	                | add rating of image per user                                               | "Rating added"
