angular.module('send', ['ngResource']).
	factory('Send', function($resource){
		return $resource('send', {}, {
			send: {method:'POST'}
		});
});

angular.module('contacts', ['ngResource']).
	factory('Contacts', function($resource){
		return $resource('contacts', {}, {
			query: {method:'GET', isArray:true}
		})
});

angular.module('contact', ['ngResource']).
	factory('Contact', function($resource){
		return $resource('contact/:id', {}, {
			add: {method:'POST', isArray:false},
			remove: {method:'GET', isArray:false}
		})
});

angular.module('account', ['ngResource']).
	factory('Account', function($resource){
		return $resource('account', {}, {
			query: {method:'GET', isArray:false},
			update: {method:'POST', isArray:false}
		})
});