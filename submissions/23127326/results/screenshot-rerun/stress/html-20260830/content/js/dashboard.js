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

    var data = {"OkPercent": 89.1473339001579, "KoPercent": 10.852666099842098};
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
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [0.891473339001579, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [1.0, 500, 1500, "CHECKOUT - create order"], "isController": false}, {"data": [1.0, 500, 1500, "CALCULATE_ORDER_TOTAL"], "isController": false}, {"data": [1.0, 500, 1500, "CART_ADD - initial quantity"], "isController": false}, {"data": [1.0, 500, 1500, "CART_UPDATE - requested quantity"], "isController": false}, {"data": [1.0, 500, 1500, "SETUP_BASE_URL"], "isController": false}, {"data": [1.0, 500, 1500, "CART_GET - verify update"], "isController": false}, {"data": [1.0, 500, 1500, "AUTH - login"], "isController": false}, {"data": [1.0, 500, 1500, "READ - search products"], "isController": false}, {"data": [0.0, 500, 1500, "POST_CHECKOUT_CART - expected empty"], "isController": false}]}, function(index, item){
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
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 16466, 1787, 10.852666099842098, 2.058180493137375, 0, 342, 1.0, 5.0, 6.0, 9.0, 34.50609923489756, 19.5030106033276, 9.73535344730936], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["CHECKOUT - create order", 1795, 0, 0.0, 4.286350974930366, 1, 34, 4.0, 7.0, 9.0, 13.0, 3.891059018369267, 1.1946132067853998, 1.602839084387207], "isController": false}, {"data": ["CALCULATE_ORDER_TOTAL", 1808, 0, 0.0, 0.5149336283185841, 0, 26, 0.0, 1.0, 1.0, 5.0, 3.8973328705969084, 0.0, 0.0], "isController": false}, {"data": ["CART_ADD - initial quantity", 1842, 0, 0.0, 2.1438653637350726, 0, 16, 2.0, 4.0, 6.0, 9.0, 3.9221364358383615, 1.1260821407582797, 1.5390379799932714], "isController": false}, {"data": ["CART_UPDATE - requested quantity", 1832, 0, 0.0, 2.078602620087335, 0, 40, 2.0, 4.0, 6.0, 8.670000000000073, 3.9216106003360767, 1.125931168455866, 1.538827784675322], "isController": false}, {"data": ["SETUP_BASE_URL", 1870, 0, 0.0, 0.7267379679144391, 0, 342, 0.0, 1.0, 2.0, 4.0, 3.92179068543254, 0.0, 0.0], "isController": false}, {"data": ["CART_GET - verify update", 1819, 0, 0.0, 1.8653106102254, 0, 13, 1.0, 4.0, 5.0, 8.0, 3.9059312607633205, 6.190463285131909, 1.2046288117186528], "isController": false}, {"data": ["AUTH - login", 1862, 0, 0.0, 2.80021482277121, 0, 29, 2.0, 5.0, 7.0, 10.0, 3.92357664987241, 2.539350180006195, 1.517333004349228], "isController": false}, {"data": ["READ - search products", 1851, 0, 0.0, 2.2290653700702303, 0, 60, 2.0, 5.0, 6.0, 9.0, 3.9213858529279046, 1.7347537025159578, 1.3396140143996], "isController": false}, {"data": ["POST_CHECKOUT_CART - expected empty", 1787, 1787, 100.0, 1.9115836597649676, 0, 17, 1.0, 4.0, 5.0, 9.0, 3.8874446631932735, 6.077805402748622, 1.1989400690146512], "isController": false}]}, function(index, item){
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
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": [{"data": ["Known business gap: cart not empty after checkout", 1787, 100.0, 10.852666099842098], "isController": false}]}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 16466, 1787, "Known business gap: cart not empty after checkout", 1787, "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": ["POST_CHECKOUT_CART - expected empty", 1787, 1787, "Known business gap: cart not empty after checkout", 1787, "", "", "", "", "", "", "", ""], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
