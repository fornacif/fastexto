angular.module('fastexto', ['send', 'contacts', 'contact', 'account', 'ui']).
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
	$scope.alerts = [
    { type: 'error', msg: 'Error sending SMS' }, 
  ];

	$scope.reset = function() {
		$scope.phonenumber = "";
		$scope.message = "";
		$scope.messageNumber = 0;
		$scope.messageLength = 0;
  }

	$scope.reset();
	$scope.contacts = Contacts.query();
	
	$scope.sendSMS = function() {
		$.blockUI({"message" : "<h3>Sending SMS...</h3>"});
		Send.send({phonenumber: $scope.phonenumber, message: $scope.message},
			function (data) {
				$.unblockUI();
				$scope.reset();
			},
			function (data) {  
				$.unblockUI();
			});
  };
  
  $scope.change = function() {
		if ($scope.message) {
			$scope.messageLength = $scope.message.length;
			$scope.messageNumber = Math.round($scope.messageLength / 160) + 1;
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
  }

	$scope.contacts = Contacts.query();
	
	$scope.add = function() {
		$.blockUI({"message" : "<h3>Adding contact...</h3>"});
		Contact.add({name: $scope.name, phonenumber: $scope.phonenumber},
			function (data) {
				$.unblockUI();
				$scope.reset();
				$scope.contacts = Contacts.query();
			},
			function (data) {  
				$.unblockUI();
			});
  };
  
  $scope.remove = function(id) {
		$.blockUI({"message" : "<h3>Deleting contact...</h3>"});
		Contact.remove({id:id},
			function (data) {
				$.unblockUI();
				$scope.contacts = Contacts.query();
			},
			function (data) {  
				$.unblockUI();
			});
  };
}

function AccountController($scope, Account) {
  $scope.account = Account.query();
  
  $scope.update = function() {
		$.blockUI({"message" : "<h3>Updating account...</h3>"});
		Account.update($scope.account,
			function (data) {
				$.unblockUI();
			},
			function (data) {  
				$.unblockUI();
			});
  };
}