var app = angular.module("Tutor", ['ui.bootstrap'])
app.factory('Test_Data', function($http, $q){
	return {
		register : function(val) {
			return $http.post("/register/",val)
			.then(function(response) {
				if (typeof response.data === 'object') {
  					return response.data['msg'];
  				} else { return "Error"; }
		}, function(error) {
  			return "Unrechable. Please try again";
			});
		},


		login : function(val) {
			return $http.post("/login/",val)
			.then(function(response) {
				if (typeof response.data === 'object') {
  					return response.data['msg'];
  				} else { return "Error"; }
		}, function(error) {
  			return "Unrechable. Please try again";
			});
		},

		logout : function() {
			return $http.post("/logout/")
			.then(function(response) {
				if (typeof response.data === 'object') {
  					return response.data['msg'];
  				} else { return "Error"; }
		}, function(error) {
  			return "Unrechable. Please try again";
			});
		},


		get_test_data : function() {
			return $http.post("/get_test/")
            .then(function(response) {
                if (typeof response.data === 'object') {
                    //alert(JSON.stringify(response.data));
                    return response.data;
                } else {
                    // invalid response
                    return $q.reject(response.data);
                }

            }, function(response) {
                // something went wrong
                return $q.reject(response.data);
                alert("Error");
        	});
		}
	};
});


app.factory('Profile_Data', function($http, $q){ 
	return {
		create_class : function(val) {
			//alert(JSON.stringify(val));
			return $http.post("/create_class/",val)
			.then(function(response) {
				if (typeof response.data === 'object') {
  					return response.data;
  				} else { return "Error"; }
				}, function(error) {
  				return null;
			});
		},

		add_students : function(val) {
			return $http.post("/add_studnet/",val)
			.then(function(response) {
				if (typeof response.data === 'object') {
  					return response.data;
  				} else { return "Error"; }
				}, function(error) {
  				return null;
			});
		},

		create_test : function(val) {
			//alert(JSON.stringify(val));
			return $http.post("/create_test/",val)
			.then(function(response) {
				if (typeof response.data === 'object') {
  					return response.data;
  				} else { return "Error"; }
				}, function(error) {
  				return null;
			});
		},

		get_all_classes : function(val) {
			//alert(JSON.stringify(val));
			return $http.post("/get_user_classes/",val)
			.then(function(response) {
				if (typeof response.data === 'object') {
					//alert(JSON.stringify(response.data))
  					return response.data;
  				} else { return "Error"; }
				}, function(error) {
  				return null;
			});
		},

		send_mail_to_class : function(val) {
			//alert(JSON.stringify(val));
			return $http.post("/send_mail_to_class/",val)
			.then(function(response) {
				if (typeof response.data === 'object') {
  					return response.data;
  				} else { return "Error"; }
				}, function(error) {
  				return null;
			});
		},

		get_basic_user_info : function() {
			return $http.get("/user_profile/")
			.then(function(response) {
				if (typeof response.data === 'object') {
  					return response.data;
  				} else { return "Error"; }
				}, function(error) {
  				return null;
			});
		},


		get_tests : function() {
			return $http.get("/get_all_tests/")
			.then(function(response) {
				if (typeof response.data === 'object') {
  					return response.data;
  				} else { return "Error"; }
				}, function(error) {
  				return null;
			});
		},

		get_solved_tests : function() {
			return $http.get("/get_user_solved_tests/")
			.then(function(response) {
				if (typeof response.data === 'object') {
  					return response.data;
  				} else { return "Error"; }
				}, function(error) {
  				return null;
			});
		},

		get_testwise_student_info : function(test_id) {
			data = {"test_id" : test_id}
			return $http.post("/testwise_students_info/", data)
			.then(function(response) {
				if (typeof response.data === 'object') {
  					return response.data;
  				} else { return "Error"; }
				}, function(error) {
  				return null;logo
			});
		},

		// For Teachers

		get_all_students : function() {
			return $http.get("/student_score/")
			.then(function(response) {
				if (typeof response.data === 'object') {
  					return response.data;
  				} else { return "Error"; }
				}, function(error) {
  				return null;
			});
		},

		save_test_id : function(id) {
			val = {"id" : id};
			return $http.post("/save_test_id/",val)
			.then(function(response) {
				if (typeof response.data === 'object') {
  					return response.data;
  				} else { return "Error"; }
				}, function(error) {
  				return null;
			});
		},

		clear_test_id : function() {
			return $http.get("/clear_test_id/")
			.then(function(response) {
				if (typeof response.data === 'object') {
  					return response.data;
  				} else { return "Error"; }
				}, function(error) {
  				return null;
			});
		},

	};
});


app.factory('Analytics_Factory', function($http, $q){
	return {
		get_overall_percentage : function(val) {
			return $http.post("/overall_percentage/",val)
			.then(function(response) {
				if (typeof response.data === 'object') {
					//alert(response.data['percentage']);
  					return response.data['percentage'];
  				} else { return "Error"; }
				}, function(error) {
  				return null;
			});
		},

		get_analytics : function(val) {
			return $http.post("/get_analytics/",val)
			.then(function(response) {
				if (typeof response.data === 'object') {
					//alert(response.data['percentage']);
  					return response.data;
  				} else { return "Error"; }
				}, function(error) {
  				return null;
			});
		},
	};
});

app.controller('Login_Manager', function($scope, $http, Test_Data,$location, $rootScope){
	this.username = "";
	this.password = "";
	this.full_name = "";
	this.register = false;
	this.register_button = "Login"
	$scope.error_msg = "";
	this.user_type = "";

	this.register_event = function() {
		this.register = true;
	};

	this.register_user = function() {
		var int_user_type = parseInt(this.user_type);
		//alert(this.user_type);
		val = {"email" : this.username , "password" : this.password, "name" : this.full_name, "user_type" : int_user_type};
		Test_Data.register(val).then(function(data) {
			if(data == "Success") {
				window.location = "http://127.0.0.1:8000/dashboard/";
			}else {
				$scope.error_msg = data;
			}
		}, function(error) {
       		$scope.error_msg = "Error Occoured"; 
        });
	};

	this.login_user = function() { 
		val = {"email" : this.username , "password" : this.password};
		Test_Data.login(val).then(function(data) {
			//alert(data);
			if(data == "Success") {
				window.location = "http://127.0.0.1:8000/dashboard/";
			}else {
				$scope.error_msg = data;
			}
		}, function(error) {
       		$scope.error_msg = "Error Occoured"; 
        });
	};

	this.logout_user = function() {
		Test_Data.logout().then(function(data) {
			alert("Successfully Logged Out");
			window.location = "http://127.0.0.1:8000/";
		}, function(error) {
       		$scope.error_msg = "Error Occoured"; 
        });
	}

});

app.controller('Data_Manager', function($scope, $http){
	this.update_state = function(state) {;
		this.current_flow_state = state;
	};

	this.get_test = function() {
		data = {"test_id" :14};
		return_json = $http.post("http://127.0.0.1:8000/get_test/",data);
		//alert(return_json);
	}

	this.graph_generate = function() {
		$scope.total_percentage = 50
		var chart = c3.generate({
	    data: {
	        columns: [
	            ['data', $scope.total_percentage]
	        ],
	        type: 'gauge',
	        onclick: function (d, i) { console.log("onclick", d, i); },
	        onmouseover: function (d, i) { console.log("onmouseover", d, i); },
	        onmouseout: function (d, i) { console.log("onmouseout", d, i); }
	    },
	    gauge: {
	    },
	    color: {
	        pattern: ['#FF0000', '#F97600', '#F6C600', '#60B044'], // the three color levels for the percentage values.
	        threshold: {
	            values: [30, 60, 90, 100]
	        }
	    },
	    size: {
	        height: 180
	    }
	});
	}
	this.graph_generate();
	this.get_test();
});

app.controller('Profile_Data_Manager', function($scope, $http, Profile_Data, Test_Data, Analytics_Factory){
	$scope.User_Profile_Basics = {};
	$scope.Tests_Info = [];
	$scope.Testwise_Student_Info = [];
	$scope.Test_Analytics_Info = {};
	$scope.total_percentage = 0;
	this.email_ids
	this.class_name
	this.analytics_view = false;
	$scope.selected_class = {};
	$scope.class_id = 0;
	$scope.class_list = [];
	/*
	this.current_view : 0  - default options 
	this.current_view : 1  - create class view
	this.current_view : 2  - add students to class
	*/
	this.current_view = 0;



	this.populate_classes = function(){
		Profile_Data.get_all_classes().then(function(data) {
			$scope.class_list = data['classes'];
		}, function(error) {
       		$scope.error_msg = "Error Occoured"; 
       });
	};


	this.back_press = function() {
		this.current_view = 0;
	};

	this.create_class_press = function() {
		this.current_view = 1;
	};

	this.add_student_press = function() {
		this.current_view = 2;
		this.populate_classes();
	};

	this.create_class = function() {
		var users = this.email_ids.split(',');
		var class_name = this.class_name;
		var req_data = {"name" : this.class_name, "users" : users};
		//alert(JSON.stringify(req_data));
		Profile_Data.create_class(req_data).then(function(data) {
			val = {"class_id" : data['class_id'] , "class_name" : class_name}
			$scope.class_list.push(val);
			alert("Class Creation Successfully");
			this.current_view = 0
			}, function(error) {
   			$scope.error_msg = "Error Occoured"; 
   		});
	};

	$scope.send_mail_to_class =function() {
		val = {"class_id" : $scope.class_id};
		//val = {"class_id" : 4};
		Profile_Data.send_mail_to_class(val).then(function(data){
			alert('Mail Sent Successfully');
		},function(error){
			alert("Error");
		});
	}

	$scope.user_display_test_mapper = function() {
		$scope.Unsolved_Tests_Info = [];
		//alert("IN");
		for (all_test in $scope.Tests_Info) {
			found = false;
			for (user_test in $scope.User_Tests_Info) {
				if (all_test.id === user_test.id) {
					found = true;
					break;
				}
			}
			if (!found) {
				$scope.Unsolved_Tests_Info.push(all_test);
			}
		}	
	}; 

	//BOth
	this.get_basic_information = function() {
		Profile_Data.get_basic_user_info().then(function(data) {
			$scope.User_Profile_Basics = data;
		}, function(error) {
       		alert("Error Occoured"); 
        });
	};


	//Both
	this.get_tests = function() {
		Profile_Data.get_tests().then(function(data) {
			$scope.Tests_Info = data['test_info'];
		}, function(error) {
       		alert("Error Occoured"); 
        });
	};

	// Student
	this.get_user_solved_tests = function() {
		Profile_Data.get_solved_tests().then(function(data) {
			$scope.User_Tests_Info = data['test_info'];
			//$scope.user_display_test_mapper();
		}, function(error) {
       		alert("Error Occoured"); 
        });
	};

	//TEacer
	this.get_testwise_student_info = function(location_index) {
		test_id = $scope.Tests_Info[parseInt(location_index)].id;
		//alert("Test id is :" + test_id);
		Profile_Data.get_testwise_student_info(test_id).then(function(data) {
			$scope.Testwise_Student_Info = data;
			//alert(JSON.stringify(data));
		}, function(error) {
       		alert("Error Occoured"); 
        });
	};

	// For Teacher
	this.get_all_students = function() {
		Profile_Data.get_all_students().then(function(data) {
			$scope.Student_Info = data;
			//alert(JSON.stringify(data));
		}, function(error) {
       		alert("Error Occoured"); 
        });
	};

	//Studnet
	this.save_test_id = function(location_index) {
		test_id = $scope.Tests_Info[parseInt(location_index)].id;
		//alert("IN" + test_id);
		Profile_Data.save_test_id(test_id).then(function(data) {
			window.location = "http://127.0.0.1:8000/start_test/";
			},function(error) {
				alert("Error Occoured"); 	
		});
	};

	this.save_retest_id = function(location_index) {
		test_id = $scope.User_Tests_Info[parseInt(location_index)].id;
		//alert("IN" + test_id);
		Profile_Data.save_test_id(test_id).then(function(data) {
			window.location = "http://127.0.0.1:8000/start_test/";
			},function(error) {
				alert("Error Occoured"); 	
		});
	};

	this.logout_user = function() {
		Test_Data.logout().then(function(data) {
			alert("Successfully Logged Out");
			window.location = "http://127.0.0.1:8000/";
		}, function(error) {
       		$scope.error_msg = "Error Occoured"; 
       });
	};

	$scope.graph_generate_gauge = function() {
		var chart = c3.generate({
	    bindto: '#chart_percentage',
	    data: {
	        columns: [
	            ['acquired percentage', $scope.total_percentage]
	        ],
	        type: 'gauge',
	        onclick: function (d, i) { console.log("onclick", d, i); },
	        onmouseover: function (d, i) { console.log("onmouseover", d, i); },
	        onmouseout: function (d, i) { console.log("onmouseout", d, i); }
	    },
	    gauge: {
	    },
	    color: {
	        pattern: ['#FF0000', '#F97600', '#F6C600', '#60B044'], // the three color levels for the percentage values.
	        threshold: {
	            values: [30, 60, 90, 100]
	        }
	    },
	    size: {
	        height: 180
	    }
	});
	}

	$scope.graph_generate_donut = function() {
		var chart = c3.generate({
		    bindto : '#chart_donut',
		    data: {
		        columns: [
		            ['Unsolved Questions', $scope.Test_Analytics_Info['DONUT']['unsolved']],
		            ['Correct', $scope.Test_Analytics_Info['DONUT']['correct']],
		            ['Incorrect', $scope.Test_Analytics_Info['DONUT']['incorrect']],
		        ],
		        type : 'donut',
		        onclick: function (d, i) { console.log("onclick", d, i); },
		        onmouseover: function (d, i) { console.log("onmouseover", d, i); },
		        onmouseout: function (d, i) { console.log("onmouseout", d, i); }
		    },
		    donut: {
		        title: "Resultwise breakup"
		    }
		});
	}
	
	$scope.graph_generate_time_taken = function() {
		var chart = c3.generate({
		    bindto : '#chart_time_taken',
		    data: {
		        columns: [
		            $scope.Test_Analytics_Info["TIME_TAKEN_PER_QUESTION"]["You"],
		            $scope.Test_Analytics_Info["TIME_TAKEN_PER_QUESTION"]["Topper"]
		        ],
		        types: {
		            data1: 'area-spline',
		            data2: 'area-spline'
		            // 'line', 'spline', 'step', 'area', 'area-step' are also available to stack
		        },
		        groups: [['data1', 'data2']]
		    }
		});
	}
		
	$scope.graph_generate_rank =function(){
		var chart = c3.generate({
		    bindto : '#chart_rank',
		    data: {
		        columns: [
		            $scope.Test_Analytics_Info["STUDENT_RANKS"]["scores"]
		        ],
		        type: 'spline'
		    }
		});
	}

	this.view_analytics = function(location_index) {
		this.analytics_view = true;
		test_summary_id = $scope.User_Tests_Info[parseInt(location_index)].summary_id;
		req_data = {"test_summary_id" : test_summary_id}
		Analytics_Factory.get_analytics(req_data).then(function(data){
			$scope.Test_Analytics_Info = data
			$scope.graph_generate_donut();
			$scope.graph_generate_rank();
			$scope.graph_generate_time_taken();
			$scope.user_display_test_mapper();
		}, function(error){
			alert("Error in gethering data. Please Try Again");
		});
	};

	this.get_overall_percentage = function() {
		Analytics_Factory.get_overall_percentage().then(function(data){
			//alert(data);
			$scope.total_percentage = data;
			$scope.graph_generate_gauge();
		}, function(error){
			alert("Error in gethering data. Please Try Again");
		});
	}

	this.select_class = function(val) {
		$scope.selected_class = $scope.class_list[val];
		$scope.class_id = $scope.selected_class['class_id'];
	};


	this.add_Student_to_class = function() {
		email_list = this.email_ids.split(',');
		if ($scope.class_id == 0) {
			alert("Select a class. Please");
			return false;
		}
		val = {"name" : this.class_name, "users" : email_list, "class_id" : $scope.class_id}
		Profile_Data.add_students(val).then(function(data){
			alert("Added Successfully");
			this.current_view = 0;
		},function(error){
			alert("Error");
		});
	}

	this.setup_profile_page = function() {
		this.get_basic_information();
		this.get_tests();
		this.get_user_solved_tests();
		this.get_all_students();
		this.get_overall_percentage();
	};
	this.setup_profile_page();
});


app.controller('Test_Preload_Manager',function(Test_Data){
	this.logout_user = function() {
		Test_Data.logout().then(function(data) {
			alert("Successfully Logged Out");
			window.location = "http://127.0.0.1:8000/";
		}, function(error) {
       		$scope.error_msg = "Error Occoured"; 
       });
	};
});


app.controller('Test_Creation_Manager', function($scope, $http, Test_Data, Profile_Data){
	$scope.class_list = [];
	$scope.selected_class = {'class_name' : "Select a Class"};
	$scope.class_id = 0;
	this.MODE = {
		"PRE_TEST_CREATE" : 1,
		"QUESTIONS_CREATE" : 2,
		"POST_TEST_CREATE" : 3
	};
	this.current_question = 1;
	this.current_flow_state = "Profile";
	this.mode = 1;
	this.question_no = 1;
	this.pre_test = {};
	this.question_obj = {
		"options" : [{},{},{},{}]
	};
	this.post_test = {};

	this.question_queue = [];
	
	this.new_question = function() {
		this.current_question = {}; 
	};

	this.select_class = function(val) {
		$scope.selected_class = $scope.class_list[val];
		$scope.class_id = $scope.selected_class['class_id'];
	};

	this.clear_selection =function() {
		$scope.selected_class = {'class_name' : "Select a Class"};
		$scope.class_id = 0;
	}
	this.add_to_queue = function() {
		//alert(JSON.stringify(this.question_obj));
		this.question_queue.push(this.question_obj);
		this.question_obj = {"options" : [{},{},{},{}]};
		this.question_no = this.question_no + 1;
	};

	this.update_mode = function() {
		//alert(JSON.stringify(this.pre_test))
		this.mode ++;
	};


	this.create_class = function() {
		var users = this.class_email.split(',');
		var class_name = this.class_name;
		var req_data = {"name" : this.class_name, "users" : users};
		//alert(JSON.stringify(req_data));
		Profile_Data.create_class(req_data).then(function(data) {
			val = {"class_id" : data['class_id'] , "class_name" : class_name}
			$scope.class_list.push(val);
			alert("Class Creation Successfully");
			}, function(error) {
   			$scope.error_msg = "Error Occoured"; 
   		});
	};


	this.submit_test = function() {
		$scope.Test_Data = {"PRE_TEST"  : {},
					"POST_TEST" : {},
					"QUESTIONS" : {},
					"CLASS_INFO" : 0};
		$scope.Test_Data["PRE_TEST"] = this.pre_test;
		$scope.Test_Data["POST_TEST"] = this.post_test;	
		$scope.Test_Data["QUESTIONS"] = this.question_queue;
		if ($scope.class_id === 0) {
			alert("Cannot proceed with save. Please select a Class");
			return false;
		}
		$scope.Test_Data["CLASS_INFO"] = $scope.class_id
		Profile_Data.create_test($scope.Test_Data).then(function(data) {
			alert("Test Creation Successfully");
			window.location = "http://127.0.0.1:8000/dashboard/";

		},function(error) {
			$scope.error_msg = "Error Occoured"; 
		});
	};


	this.logout_user = function() {
		Test_Data.logout().then(function(data) {
			alert("Successfully Logged Out");
			window.location = "http://127.0.0.1:8000/";
		}, function(error) {
       		$scope.error_msg = "Error Occoured"; 
       });
	};
	
	this.populate_classes = function(){
		Profile_Data.get_all_classes().then(function(data) {
			$scope.class_list = data['classes'];
		}, function(error) {
       		$scope.error_msg = "Error Occoured"; 
       });
	};

	this.show_view = function(val) {
		this.mode = val;
	};
	this.populate_classes();
});

app.controller('Test_Manager', function($scope, $http, $timeout, Test_Data, $rootScope){
	$scope.current_question_id = 1;
	$scope.traverse_id_map = {};
	$scope.forward_counter = 0;

	this.answered = [];
	this.user_answers = {"answers" : []};
	this.user_selection = {"id" : 0, "selected" : [], "time_taken" : 0};
	this.unanswered = [];
	this.questions_list_unapplied = {};
	this.question_button = [];
	this.item = {};
	this.dummyVal = "";

	

    var mytimeout = null; // the current timeoutID
    // actual timer method, counts down every second, stops on zero

	this.populate_test = function() {
		Test_Data.get_test_data().then(function(data) {
			$scope.test_name = data['test_name']
			$scope.questions_list = data['questions'];
			$scope.test_id = data['test_id'];
			$scope.reverse_counter = parseInt(data['total_time']);
			$scope.minutes = Math.round($scope.reverse_counter / 60);
			$scope.seconds = Math.round($scope.reverse_counter % 60);
			$scope.hours = Math.round($scope.minutes/ 60);
			$scope.startTimer();

			$scope.question_time_spent = {};
			count = 1;
			for (var item in data['questions']) {
				$scope.question_time_spent[count] = 0;
				$scope.traverse_id_map[item] = count;
				count++;
			}

		}, function(error) {
       		alert("Error");
        });
	};
	
	this.logout_user =function() {
		Test_Data.logout().then(function(data) {
			alert("Successfully Logged Out");
			window.location = "http://127.0.0.1:8000/";
		}, function(error) {
       		$scope.error_msg = "Error Occoured"; 
        });
	};

	this.mark_question = function(id) {
		$scope.questions_list[id].class = "mark";
	};

	this.previous = function() {
		if(this.current_question_id > 1) {
			$scope.current_question_id = $scope.current_question_id - 1;
		}
	};

	this.next = function() {
		$scope.current_question_id = $scope.current_question_id +1;
	};

	this.result = function() {
		var str = JSON.stringify(this.question_queue);
		//alert(str);
	};

	this.set_id = function(id) {
		$scope.current_question_id = id;
	};

	$scope.onTimeout = function() {
        if($scope.reverse_counter ===  0) {
            $scope.$broadcast('timer-stopped', 0);
            $timeout.cancel(mytimeout);
            return;
        }
        $scope.reverse_counter--;
        $scope.forward_counter++;
        $scope.minutes = Math.round($scope.reverse_counter / 60);
		$scope.seconds = Math.round($scope.reverse_counter % 60);
		$scope.hours = Math.round($scope.minutes/ 60);
		$scope.question_time_spent[$scope.current_question_id]++;
        mytimeout = $timeout($scope.onTimeout, 1000);
    };
    $scope.startTimer = function() {
        mytimeout = $timeout($scope.onTimeout, 1000);
    };
    // stops and resets the current timer
    $scope.stopTimer = function() {
        $scope.$broadcast('timer-stopped', $scope.reverse_counter);
        $timeout.cancel(mytimeout);
    };
    // triggered, when the timer stops, you can do something here, maybe show a visual indicator or vibrate the device

    this.get_results = function() {
		$scope.stopTimer();
		for ( var key in $scope.questions_list) {
			this.user_selection["id"] = key;
			for (var i = 0 ; i < $scope.questions_list[key].options.length ; i++) {
				if ($scope.questions_list[key].options[i].correct) {
					this.user_selection.selected.push($scope.questions_list[key].options[i].option);
				}
			}
			time_taken = $scope.question_time_spent[$scope.traverse_id_map[key]]
			this.user_selection.time_taken = time_taken
			this.answered.push(this.user_selection);
			this.user_selection = {"id" : 0, "selected" : [], "time_taken" : 0};
		}

		data_obj = {"test_id" : $scope.test_id, "total_time_taken" : $scope.forward_counter , "answers" : this.answered}
		
		//alert(JSON.stringify(data_obj));
		
		$http.post("/get_result/",data_obj).
		success(function(data, status, headers, config) {
  			alert("Score : " + data.user_score + "/" + data.total_score);
  			window.location = "http://127.0.0.1:8000/dashboard/";
		}).
		error(function(data, status, headers, config) {
  			alert("ERROR");
		});

	};

	$scope.$on('timer-stopped', function(event, remaining) {
        if(remaining === 0) {
            alert('your time ran out!. Your Responses will be submitted automatically');
            this.get_results();
        }
    });

	this.populate_test();
});

