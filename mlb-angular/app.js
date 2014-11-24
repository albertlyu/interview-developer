var App = angular.module('App', []);
 
App.controller('RosterCtrl', function($scope, $http) {
  $http.get('roster.json')
       .then(function(res){
          $scope.players = res.data;                
        });
});