angular.module('InspireApp').controller('AddReportController', function($rootScope, $scope, $http, $state, $stateParams, $q) {

    $scope.is_edit = false;

    if ($stateParams.reportId != undefined) {
        $scope.is_edit = true;
    }
    $scope.report = {};
    $scope.step = "1";
    $scope.isDisabled = false;
    $scope.dimensions = [];
    $scope.communities = [];
    $scope.metrics = [];
    $scope.interests = []

    function create_new_report() {
        var report = {
            "type": 'sale',
            "metrics": _.filter($scope.metrics, {
                'default': true
            }),
            "country": _.find($scope.countries, {
                'id': 'US'
            }),
            "email_metrics": [{
                'name': 'AS Emails Sent',
                'code': 'n_sent',
                'group': 'email'
            }, {
                'name': 'AS Emails Opened',
                'code': 'n_opened',
                'group': 'email'
            }, {
                'name': 'AS Emails Clicked',
                'code': 'n_clicked',
                'group': 'email'
            }],
            "include_cpm": true,
            "include_cps": true
        };
        return report;
    };

    $scope.save = function() {
        console.log($scope.report);
        $http({
            method: $scope.is_edit ? 'PUT' : 'POST',
            url: ($scope.is_edit ? '/dfp/report/' + $stateParams.reportId : '/dfp/reports/'),
            data: angular.toJson($scope.report)
        }).then(function successCallback(response) {
            $state.go('dashboard');
        });
    };

    function load_dimensions() {
        return $http({
            method: 'GET',
            url: '/dfp/dimensions'
        }).then(function successCallback(response) {
            $scope.dimensions = response.data.result;
        });
    }

    function load_metrics() {
        return $http({
            method: 'GET',
            url: '/dfp/metrics'
        }).then(function successCallback(response) {
            $scope.metrics = response.data.result;
        });
    };

    function load_countries() {
        return $http({
            method: 'GET',
            url: '/dfp/countries'
        }).then(function successCallback(response) {
            $scope.countries = response.data.result;
        });
    };

    function load_communities() {
        return $http({
            method: 'GET',
            url: '/dfp/communities'
        }).then(function successCallback(response) {
            $scope.communities = response.data.result;
        });
    };

    function initialize_report() {
        if ($stateParams.reportId) {
            $http({
                method: 'GET',
                url: '/dfp/report/config/' + $stateParams.reportId,
                data: angular.toJson($scope.report)
            }).then(function successCallback(response) {
                $scope.report = response.data.data.job;
            });
        } else {
            $scope.report = create_new_report();
        }
    };

    $scope.intialize_report_options = function() {
        $('.date-picker').datepicker({
            autoclose: true,
            clearBtn: true,
            todayHighlight: true
        });
    }
    $scope.setStep = function(value) {
        console.log($scope.step);
        if (value == '2' && $scope.report.type == 'sale') {
            $scope.step = '3';
        } else if (value == '4') {
            $scope.step = '4';
        } else {
            $scope.step = value;
        }
    };


    $scope.email_metrics = [{
        'name': 'AS Emails Sent',
        'code': 'n_sent',
        'group': 'email'
    }, {
        'name': 'AS Emails Opened',
        'code': 'n_opened',
        'group': 'email'
    }, {
        'name': 'AS Emails Clicked',
        'code': 'n_clicked',
        'group': 'email'
    }, {
        'name': 'AS Number of Clicks',
        'code': 'n_clicks',
        'group': 'email'
    }, {
        'name': 'Market Research',
        'code': 'market_research',
        'group': 'market_research'
    }, {
        'name': 'Offers',
        'code': 'offers',
        'group': 'offer'
    }];


    $scope.refresh_interests = function(value) {
        console.log(value);
        if (value) {
            $http({
                method: 'GET',
                url: '/dfp/search/?interest=' + value,
            }).then(function successCallback(response) {
                console.log(response.data);
                $scope.interests = response.data.result;
            });
        }

    }

    $scope.$on('$viewContentLoaded', function() {
        // initialize core components
        App.initAjax();
        var p_countries = load_countries();
        var p_metrics = load_metrics();
        $('.bs-select').selectpicker();
        var p_dims = load_dimensions();
        var p_communities = load_communities();
        var all = $q.all([p_countries, p_metrics, p_dims, p_dims, p_communities])
        all.then(function() {
            initialize_report();
        });
    });

    $rootScope.settings.layout.pageContentWhite = true;
    $rootScope.settings.layout.pageBodySolid = false;
    $rootScope.settings.layout.pageSidebarClosed = false;
});