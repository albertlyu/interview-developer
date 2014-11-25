var App = angular.module('App', []);

// Controller for roster data
App.controller('RosterCtrl', ['$scope', '$http', function($scope, $http) {
  $http.get('roster.json')
    .then(function(res) {
      $scope.players = res.data;
      $scope.players.forEach(function(player) {
        player.fullname = player.firstname + ' ' + player.lastname;
        player.batthrow = player.bats + '/' + player.throws;
        player.notes = [];
        player.text = '';
        player.submit = function() {
          if (player.text) {
            var dateString = new Date().toLocaleString();
            player.notes.push(dateString + ': ' + this.text);
            player.text = '';
          }
          console.log(player);
          console.log(player.notes);
        };
      });
      console.log($scope.players);
      $scope.Math = Math;
    });
}]);

// Directive for default player image
App.directive('errSrc', function() {
  return {
    link: function(scope, element, attrs) {
      element.bind('error', function() {
        if (attrs.src != attrs.errSrc) {
          attrs.$set('src', attrs.errSrc);
        }
      });
    }
  };
});

// Filter for calculating age based on date of birth
App.filter('ageFilter', function() {
  function calculateAge(dateOfBirth) {
    var birthdate = new Date(dateOfBirth);
    var ageDifMs = Date.now() - birthdate.getTime();
    var ageDate = new Date(ageDifMs);
    return Math.abs(ageDate.getUTCFullYear() - 1970);
  }
  return function(birthdate) {
    return calculateAge(birthdate);
  };
});
