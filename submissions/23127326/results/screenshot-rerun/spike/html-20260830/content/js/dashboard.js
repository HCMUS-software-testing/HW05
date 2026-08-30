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

    var data = {"OkPercent": 89.52952673460841, "KoPercent": 10.470473265391595};
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
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [0.895295267346084, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [1.0, 500, 1500, "CHECKOUT - create order"], "isController": false}, {"data": [1.0, 500, 1500, "CALCULATE_ORDER_TOTAL"], "isController": false}, {"data": [1.0, 500, 1500, "CART_ADD - initial quantity"], "isController": false}, {"data": [1.0, 500, 1500, "CART_UPDATE - requested quantity"], "isController": false}, {"data": [1.0, 500, 1500, "SETUP_BASE_URL"], "isController": false}, {"data": [1.0, 500, 1500, "CART_GET - verify update"], "isController": false}, {"data": [1.0, 500, 1500, "AUTH - login"], "isController": false}, {"data": [1.0, 500, 1500, "READ - search products"], "isController": false}, {"data": [0.0, 500, 1500, "POST_CHECKOUT_CART - expected empty"], "isController": false}]}, function(index, item){
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
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 7163, 750, 10.470473265391595, 2.2355158453162134, 0, 357, 2.0, 5.0, 7.0, 10.0, 17.131158714935893, 7.476026927075984, 4.809840128567397], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["CHECKOUT - create order", 756, 0, 0.0, 4.461640211640215, 1, 14, 4.0, 8.0, 9.0, 12.0, 1.8986435748746167, 0.581936374720917, 0.7817522866600198], "isController": false}, {"data": ["CALCULATE_ORDER_TOTAL", 762, 0, 0.0, 0.7309711286089245, 0, 23, 1.0, 1.0, 2.0, 5.0, 1.8827878108020626, 0.0, 0.0], "isController": false}, {"data": ["CART_ADD - initial quantity", 811, 0, 0.0, 2.255240443896427, 0, 20, 2.0, 4.0, 6.0, 9.0, 1.9813445780542267, 0.5688626034647878, 0.777145420858599], "isController": false}, {"data": ["CART_UPDATE - requested quantity", 792, 0, 0.0, 2.275252525252525, 0, 13, 2.0, 5.0, 7.0, 9.069999999999936, 1.9356683554884262, 0.5557485317515599, 0.7592136713909683], "isController": false}, {"data": ["SETUP_BASE_URL", 848, 0, 0.0, 1.1143867924528317, 0, 357, 1.0, 1.0, 2.0, 5.509999999999991, 2.0294606851823045, 0.0, 0.0], "isController": false}, {"data": ["CART_GET - verify update", 774, 0, 0.0, 2.010335917312663, 0, 22, 1.0, 4.0, 6.0, 8.0, 1.9097059447616322, 1.9173898164128615, 0.588634204030121], "isController": false}, {"data": ["AUTH - login", 841, 0, 0.0, 2.9357907253269913, 0, 19, 2.0, 6.0, 8.0, 10.580000000000041, 2.025959259187882, 1.3107155418296748, 0.7667828953390892], "isController": false}, {"data": ["READ - search products", 829, 0, 0.0, 2.285886610373943, 0, 28, 2.0, 5.0, 6.0, 9.700000000000045, 2.0092001492964164, 0.8888356129211686, 0.6860519489726177], "isController": false}, {"data": ["POST_CHECKOUT_CART - expected empty", 750, 750, 100.0, 2.1160000000000014, 0, 12, 2.0, 5.0, 6.0, 9.0, 1.8854927672497448, 1.8755227332291704, 0.5811515890618794], "isController": false}]}, function(index, item){
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
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": [{"data": ["Known business gap: cart not empty after checkout", 750, 100.0, 10.470473265391595], "isController": false}]}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 7163, 750, "Known business gap: cart not empty after checkout", 750, "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": ["POST_CHECKOUT_CART - expected empty", 750, 750, "Known business gap: cart not empty after checkout", 750, "", "", "", "", "", "", "", ""], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
