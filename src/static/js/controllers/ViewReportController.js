angular.module('InspireApp').controller('ViewReportController', function($rootScope, $scope, $http, $timeout, $stateParams) {
    $scope.$on('$viewContentLoaded', function() {
        // initialize core components
        App.initAjax();
        $scope.fetch_data($stateParams.reportId);
    });
    console.log($stateParams);

    $scope.fetch_data = function(report_id) {	
    	$http({
                method: 'GET',
                url: '/dfp/report/' + report_id
            }).then(function successCallback(response) {
            	console.log(response.data.report);
                $scope.report = response.data.report;
               	
            });
    }
    
});