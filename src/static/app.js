(function() {

	var app = angular.module('cit', ['ngResource']);

	app.directive('contactForm', function() {
		return {
			restrict: 'AE',
			templateUrl: '/partials/contact-form.html',
			scope: {},
			controller: function($scope, $resource, $location) {
				$scope.init = function() {
					console.log('[contactForm] $scope.init()');

					$scope.name = '';
					$scope.email = '';
					$scope.message = '';

					$scope.sendSuccess = false;
				};

				$scope.sendMessage = function() {
					if ($scope.contactForm.$valid) {
						console.log('[contactForm] $scope.sendMessage()');

						var message = $resource('/api/contact', null, {
							send: {
								method: 'POST'
							}
						});

						sentMessage = message.send(null, {
							name: $scope.name,
							email: $scope.email,
							message: $scope.message
						}, function(response) {
							alert('Success! Your message has been sent.');
							$scope.sendSuccess = true;
						}, function(response) {
							// Error
							if (response.status == 400) {
								alert('Please complete the contact form. Error 400');
							} else {
								alert('There was an error sending the message.');
							}
						});
					} else {
						alert('Please complete the contact form.');
					}
				};


				// Init
				$scope.init();
			}
		};
	});

})();