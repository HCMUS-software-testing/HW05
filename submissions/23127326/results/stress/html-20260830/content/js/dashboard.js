/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
var showControllersOnly = false;
var seriesFilter = "";
var filtersOnlySampleSeries = true;

/*
 * Add header in statistics table to group metrics by category
 * format
 *
 */
function summaryTableHeader(header) {
    var newRow = header.insertRow(-1);
    newRow.className = "tablesorter-no-sort";
    var cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Requests";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 3;
    cell.innerHTML = "Executions";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 7;
    cell.innerHTML = "Response Times (ms)";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Throughput";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 2;
    cell.innerHTML = "Network (KB/sec)";
    newRow.appendChild(cell);
}

/*
 * Populates the table identified by id parameter with the specified data and
 * format
 *
 */
function createTable(table, info, formatter, defaultSorts, seriesIndex, headerCreator) {
    var tableRef = table[0];

    // Create header and populate it with data.titles array
    var header = tableRef.createTHead();

    // Call callback is available
    if(headerCreator) {
        headerCreator(header);
    }

    var newRow = header.insertRow(-1);
    for (var index = 0; index < info.titles.length; index++) {
        var cell = document.createElement('th');
        cell.innerHTML = info.titles[index];
        newRow.appendChild(cell);
    }

    var tBody;

    // Create overall body if defined
    if(info.overall){
        tBody = document.createElement('tbody');
        tBody.className = "tablesorter-no-sort";
        tableRef.appendChild(tBody);
        var newRow = tBody.insertRow(-1);
        var data = info.overall.data;
        for(var index=0;index < data.length; index++){
            var cell = newRow.insertCell(-1);
            cell.innerHTML = formatter ? formatter(index, data[index]): data[index];
        }
    }

    // Create regular body
    tBody = document.createElement('tbody');
    tableRef.appendChild(tBody);

    var regexp;
    if(seriesFilter) {
        regexp = new RegExp(seriesFilter, 'i');
    }
    // Populate body with data.items array
    for(var index=0; index < info.items.length; index++){
        var item = info.items[index];
        if((!regexp || filtersOnlySampleSeries && !info.supportsControllersDiscrimination || regexp.test(item.data[seriesIndex]))
                &&
                (!showControllersOnly || !info.supportsControllersDiscrimination || item.isController)){
            if(item.data.length > 0) {
                var newRow = tBody.insertRow(-1);
                for(var col=0; col < item.data.length; col++){
                    var cell = newRow.insertCell(-1);
                    cell.innerHTML = formatter ? formatter(col, item.data[col]) : item.data[col];
                }
            }
        }
    }

    // Add support of columns sort
    table.tablesorter({sortList : defaultSorts});
}

$(document).ready(function() {

    // Customize table sorter default options
    $.extend( $.tablesorter.defaults, {
        theme: 'blue',
        cssInfoBlock: "tablesorter-no-sort",
        widthFixed: true,
        widgets: ['zebra']
    });

    var data = {"OkPercent": 89.1700466129911, "KoPercent": 10.8299533870089};
    var dataset = [
        {
            "label" : "FAIL",
            "data" : data.KoPercent,
            "color" : "#FF6347"
        },
        {
            "label" : "PASS",
            "data" : data.OkPercent,
            "color" : "#9ACD32"
        }];
    $.plot($("#flot-requests-summary"), dataset, {
        series : {
            pie : {
                show : true,
                radius : 1,
                label : {
                    show : true,
                    radius : 3 / 4,
                    formatter : function(label, series) {
                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'
                            + label
                            + '<br/>'
                            + Math.round10(series.percent, -2)
                            + '%</div>';
                    },
                    background : {
                        opacity : 0.5,
                        color : '#000'
                    }
                }
            }
        },
        legend : {
            show : true
        }
    });

    // Creates APDEX table
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [0.891700466129911, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [1.0, 500, 1500, "CHECKOUT - create order"], "isController": false}, {"data": [1.0, 500, 1500, "CALCULATE_ORDER_TOTAL"], "isController": false}, {"data": [1.0, 500, 1500, "CART_ADD - initial quantity"], "isController": false}, {"data": [1.0, 500, 1500, "CART_UPDATE - requested quantity"], "isController": false}, {"data": [1.0, 500, 1500, "SETUP_BASE_URL"], "isController": false}, {"data": [1.0, 500, 1500, "CART_GET - verify update"], "isController": false}, {"data": [1.0, 500, 1500, "AUTH - login"], "isController": false}, {"data": [1.0, 500, 1500, "READ - search products"], "isController": false}, {"data": [0.0, 500, 1500, "POST_CHECKOUT_CART - expected empty"], "isController": false}]}, function(index, item){
        switch(index){
            case 0:
                item = item.toFixed(3);
                break;
            case 1:
            case 2:
                item = formatDuration(item);
                break;
        }
        return item;
    }, [[0, 0]], 3);

    // Create statistics table
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 16519, 1789, 10.8299533870089, 2.2972334887099732, 0, 320, 2.0, 5.0, 6.0, 8.0, 34.50206043238795, 19.530972603977165, 9.73638419571079], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["CHECKOUT - create order", 1798, 0, 0.0, 4.69911012235818, 1, 23, 4.0, 7.0, 8.0, 9.0, 3.8767378480008277, 1.190220289348458, 1.5969346340870478], "isController": false}, {"data": ["CALCULATE_ORDER_TOTAL", 1809, 0, 0.0, 0.6898839137645106, 0, 25, 1.0, 2.0, 2.0, 4.0, 3.8798761184938617, 0.0, 0.0], "isController": false}, {"data": ["CART_ADD - initial quantity", 1849, 0, 0.0, 2.3472147106544106, 0, 15, 2.0, 5.0, 5.0, 6.5, 3.916202998680479, 1.124378595324278, 1.5367268629763142], "isController": false}, {"data": ["CART_UPDATE - requested quantity", 1837, 0, 0.0, 2.391399020141532, 0, 13, 2.0, 5.0, 5.0, 6.619999999999891, 3.901894022264373, 1.1202703540485601, 1.5311054313217798], "isController": false}, {"data": ["SETUP_BASE_URL", 1878, 0, 0.0, 0.8919062832800828, 0, 320, 1.0, 2.0, 2.0, 4.0, 3.9237316819395525, 0.0, 0.0], "isController": false}, {"data": ["CART_GET - verify update", 1826, 0, 0.0, 2.112267250821471, 0, 9, 2.0, 4.0, 5.0, 6.0, 3.891398857727389, 6.184822299090018, 1.2001662595366975], "isController": false}, {"data": ["AUTH - login", 1870, 0, 0.0, 3.0588235294117685, 0, 19, 3.0, 5.0, 6.0, 8.0, 3.923922075523959, 2.5395760229738293, 1.5175812889244675], "isController": false}, {"data": ["READ - search products", 1863, 0, 0.0, 2.3623188405797113, 0, 13, 2.0, 4.0, 5.0, 7.0, 3.923749107520835, 1.735799165729432, 1.3404361610179845], "isController": false}, {"data": ["POST_CHECKOUT_CART - expected empty", 1789, 1789, 100.0, 2.160424818334269, 0, 12, 2.0, 4.0, 5.0, 6.099999999999909, 3.873686216259522, 6.071883292346384, 1.1946869877759108], "isController": false}]}, function(index, item){
        switch(index){
            // Errors pct
            case 3:
                item = item.toFixed(2) + '%';
                break;
            // Mean
            case 4:
            // Mean
            case 7:
            // Median
            case 8:
            // Percentile 1
            case 9:
            // Percentile 2
            case 10:
            // Percentile 3
            case 11:
            // Throughput
            case 12:
            // Kbytes/s
            case 13:
            // Sent Kbytes/s
                item = item.toFixed(2);
                break;
        }
        return item;
    }, [[0, 0]], 0, summaryTableHeader);

    // Create error table
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": [{"data": ["Known business gap: cart not empty after checkout", 1789, 100.0, 10.8299533870089], "isController": false}]}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 16519, 1789, "Known business gap: cart not empty after checkout", 1789, "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": ["POST_CHECKOUT_CART - expected empty", 1789, 1789, "Known business gap: cart not empty after checkout", 1789, "", "", "", "", "", "", "", ""], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
