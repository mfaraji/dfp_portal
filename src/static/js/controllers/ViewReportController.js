angular.module('InspireApp').controller('ViewReportController', function($rootScope, $scope, $http, $timeout, $stateParams) {
    $scope.$on('$viewContentLoaded', function() {
        // initialize core components
        App.initAjax();
        $scope.fetch_data($stateParams.reportId);
    });
    $scope.headers = [];
    $scope.content = [];
    $scope.show_price = true;


    formatMoney = function(value, c, d, t) {
        var n = value,
            c = isNaN(c = Math.abs(c)) ? 2 : c,
            d = d == undefined ? "." : d,
            t = t == undefined ? "," : t,
            s = n < 0 ? "-" : "",
            i = String(parseInt(n = Math.abs(Number(n) || 0).toFixed(c))),
            j = (j = i.length) > 3 ? j % 3 : 0;
        return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
    };

    function format_content(data) {
        if (data == undefined){
            return;
        }
        var result = [];
        if ($scope.show_price == false) {
            return data.rows;
        }

        for (var rowIndex = 0; rowIndex < data.rows.length; rowIndex++) {
            var new_row = [];
            for (var itemIndex = 0; itemIndex < data.rows[rowIndex].length; itemIndex++) {
                if (($scope.headers[itemIndex] == "Forecasted impressions") || ($scope.headers[itemIndex] == "Available impressions")) {
                    new_row.push(formatMoney(data.rows[rowIndex][itemIndex] * data.prices[rowIndex]));
                } else {
                    new_row.push(data.rows[rowIndex][itemIndex]);
                }
            }
            result.push(new_row);
        }

        return result;
    }

    $scope.$watch('show_price', function() {
        $scope.content = format_content($scope.report);
    });

    $scope.fetch_data = function(report_id) {
        $http({
            method: 'GET',
            url: '/dfp/report/' + report_id
        }).then(function successCallback(response) {
            console.log(response.data.report);
            $scope.report = response.data.report;
            $scope.headers = response.data.report.headers;
            $scope.content = format_content(response.data.report);
        });
    }

    $scope.have_price = function() {
        return true;
    };

});