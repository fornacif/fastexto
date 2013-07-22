angular.module('fastexto', ['send', 'contacts', 'contact', 'account', 'ui.select2', 'ui.mask']).
	config(function($routeProvider) {
		$routeProvider.
			when('/', {controller:SendController, templateUrl:'static/partials/send.html'}).
			when('/contacts', {controller:ContactsController, templateUrl:'static/partials/contacts.html'}).
			when('/account', {controller:AccountController, templateUrl:'static/partials/account.html'}).
			otherwise({redirectTo:'/'});
	});

function MenuController($scope, $location) {
	$scope.isActive = function(route) {
		return route === $location.path();
	}
}
  
function SendController($scope, Contacts, Send) {
	$scope.reset = function() {
		$scope.phonenumber = "";
		$scope.message = "";
		$scope.messageNumber = 0;
		$scope.messageLength = 0;
		$scope.error = null;
  }

	$scope.reset();
	$scope.contacts = loadContacts(Contacts);
	
	$scope.sendSMS = function() {
		$.blockUI({"message" : "<h3>Sending SMS...</h3>"});
		Send.send({phonenumber: $scope.phonenumber, message: $scope.message},
			function () {
				$.unblockUI();
				$scope.reset();
			},
			function () {
				$scope.error = "Error sending SMS";
				$.unblockUI();
			});
  };
  
  $scope.change = function() {
		if ($scope.message) {
			$scope.messageLength = $scope.message.length;
			$scope.messageNumber = Math.ceil($scope.messageLength / 160);
		} else {
			$scope.messageNumber = 0;
			$scope.messageLength = 0;
		}
  };
  
}

function ContactsController($scope, Contacts, Contact) {
	$scope.reset = function() {
		$scope.name = "";
		$scope.phonenumber = "";	
		$scope.error = null;
  }

	$scope.contacts = loadContacts(Contacts);
	
	$scope.add = function() {
		$.blockUI({"message" : "<h3>Adding contact...</h3>"});
		Contact.add({name: $scope.name, phonenumber: $scope.phonenumber},
			function () {
				$.unblockUI();
				$scope.reset();
				$scope.contacts = loadContacts(Contacts);
			},
			function () {
				$scope.error = "Error adding contact";
				$.unblockUI();
			});
	};
	
	$scope.remove = function(id) {
		$.blockUI({"message" : "<h3>Deleting contact...</h3>"});
		Contact.remove({id:id},
			function () {
				$.unblockUI();
				$scope.reset();
				$scope.contacts = loadContacts(Contacts);
			},
			function () {  
				$scope.error = "Error deleting contact";
				$.unblockUI();
			});
	};
}

function AccountController($scope, Account) {
	$scope.reset = function() {
		$scope.error = null;
		$scope.account.password = null;
  }

	$.blockUI({"message" : "<h3>Loading account...</h3>"});
	$scope.account = Account.query({}, function () {
		$scope.reset();
		$.unblockUI();
	},
	function () { 
		$scope.error = "Error loading account";
		$.unblockUI();
	});

	$scope.update = function() {
		$.blockUI({"message" : "<h3>Updating account...</h3>"});
		Account.update($scope.account,
			function () {
				$.unblockUI();
				$scope.reset();
			},
			function () {  
				$scope.error = "Error updating account";
				$.unblockUI();
			});
	};
}

function loadContacts (Contacts) {
	$.blockUI({"message" : "<h3>Loading contacts...</h3>"});
	return Contacts.query({},
			function () {
				$.unblockUI();
			},
			function () {
				$.unblockUI();
			});
}