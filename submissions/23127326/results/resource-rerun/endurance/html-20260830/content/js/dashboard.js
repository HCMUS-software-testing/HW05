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

    var data = {"OkPercent": 89.0168470741434, "KoPercent": 10.983152925856597};
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
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [0.890168470741434, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [1.0, 500, 1500, "CHECKOUT - create order"], "isController": false}, {"data": [1.0, 500, 1500, "CALCULATE_ORDER_TOTAL"], "isController": false}, {"data": [1.0, 500, 1500, "CART_ADD - initial quantity"], "isController": false}, {"data": [1.0, 500, 1500, "CART_UPDATE - requested quantity"], "isController": false}, {"data": [1.0, 500, 1500, "SETUP_BASE_URL"], "isController": false}, {"data": [1.0, 500, 1500, "CART_GET - verify update"], "isController": false}, {"data": [1.0, 500, 1500, "AUTH - login"], "isController": false}, {"data": [1.0, 500, 1500, "READ - search products"], "isController": false}, {"data": [0.0, 500, 1500, "POST_CHECKOUT_CART - expected empty"], "isController": false}]}, function(index, item){
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
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 24574, 2699, 10.983152925856597, 2.443069911288351, 0, 322, 2.0, 5.0, 6.0, 7.0, 30.431331367651445, 25.778509414360332, 8.599557932483037], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["CHECKOUT - create order", 2708, 0, 0.0, 5.474889217134416, 1, 15, 6.0, 7.0, 8.0, 9.0, 3.422553973473943, 1.051470117188981, 1.4097112204286535], "isController": false}, {"data": ["CALCULATE_ORDER_TOTAL", 2717, 0, 0.0, 0.5542878174457125, 0, 11, 1.0, 1.0, 1.0, 2.0, 3.4280018672958277, 0.0, 0.0], "isController": false}, {"data": ["CART_ADD - initial quantity", 2739, 0, 0.0, 2.4220518437385903, 0, 21, 2.0, 4.0, 4.0, 6.0, 3.4238698354442407, 0.9830251285357487, 1.3433770963233713], "isController": false}, {"data": ["CART_UPDATE - requested quantity", 2730, 0, 0.0, 2.421245421245417, 0, 11, 2.0, 4.0, 4.0, 6.0, 3.4218116048296428, 0.9824341912303857, 1.3425670347620964], "isController": false}, {"data": ["SETUP_BASE_URL", 2762, 0, 0.0, 0.7089065894279517, 0, 322, 1.0, 1.0, 2.0, 3.0, 3.423706627264704, 0.0, 0.0], "isController": false}, {"data": ["CART_GET - verify update", 2722, 0, 0.0, 2.1932402645113847, 0, 14, 2.0, 4.0, 4.0, 5.0, 3.418859241470436, 9.76080457096582, 1.0542805723826008], "isController": false}, {"data": ["AUTH - login", 2753, 0, 0.0, 3.515074464220848, 0, 19, 4.0, 5.0, 6.0, 7.0, 3.4199055147063393, 2.213123378867891, 1.3343975215467712], "isController": false}, {"data": ["READ - search products", 2744, 0, 0.0, 2.595481049562681, 0, 16, 3.0, 4.0, 5.0, 6.0, 3.418943989872749, 1.5124820580198783, 1.1678275415936217], "isController": false}, {"data": ["POST_CHECKOUT_CART - expected empty", 2699, 2699, 100.0, 2.1241200444609123, 0, 11, 2.0, 3.0, 4.0, 5.0, 3.42137988472016, 9.694795210797057, 1.0550613073816366], "isController": false}]}, function(index, item){
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
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": [{"data": ["Known business gap: cart not empty after checkout", 2699, 100.0, 10.983152925856597], "isController": false}]}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 24574, 2699, "Known business gap: cart not empty after checkout", 2699, "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": ["POST_CHECKOUT_CART - expected empty", 2699, 2699, "Known business gap: cart not empty after checkout", 2699, "", "", "", "", "", "", "", ""], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
