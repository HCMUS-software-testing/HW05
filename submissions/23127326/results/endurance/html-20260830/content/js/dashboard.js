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

    var data = {"OkPercent": 89.02795838751625, "KoPercent": 10.972041612483745};
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
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [0.8902795838751626, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [1.0, 500, 1500, "CHECKOUT - create order"], "isController": false}, {"data": [1.0, 500, 1500, "CALCULATE_ORDER_TOTAL"], "isController": false}, {"data": [1.0, 500, 1500, "CART_ADD - initial quantity"], "isController": false}, {"data": [1.0, 500, 1500, "CART_UPDATE - requested quantity"], "isController": false}, {"data": [1.0, 500, 1500, "SETUP_BASE_URL"], "isController": false}, {"data": [1.0, 500, 1500, "CART_GET - verify update"], "isController": false}, {"data": [1.0, 500, 1500, "AUTH - login"], "isController": false}, {"data": [1.0, 500, 1500, "READ - search products"], "isController": false}, {"data": [0.0, 500, 1500, "POST_CHECKOUT_CART - expected empty"], "isController": false}]}, function(index, item){
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
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 24608, 2700, 10.972041612483745, 1.8875162548764512, 0, 333, 1.0, 4.0, 5.0, 7.0, 30.431492043391586, 25.796152119896963, 8.601404430964612], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["CHECKOUT - create order", 2715, 0, 0.0, 4.3392265193370285, 1, 25, 4.0, 6.0, 7.0, 10.0, 3.422408392274811, 1.0514289145923175, 1.409643356525455], "isController": false}, {"data": ["CALCULATE_ORDER_TOTAL", 2719, 0, 0.0, 0.43361529974255264, 0, 22, 0.0, 1.0, 1.0, 2.800000000000182, 3.4211542841181184, 0.0, 0.0], "isController": false}, {"data": ["CART_ADD - initial quantity", 2743, 0, 0.0, 1.8596427269413025, 0, 24, 2.0, 3.0, 4.0, 7.0, 3.4205748261654647, 0.9820791004811001, 1.3420780779250092], "isController": false}, {"data": ["CART_UPDATE - requested quantity", 2733, 0, 0.0, 1.8547383827295951, 0, 24, 2.0, 3.0, 4.0, 6.0, 3.4195969304957226, 0.9817983374665454, 1.341696486217135], "isController": false}, {"data": ["SETUP_BASE_URL", 2764, 0, 0.0, 0.5676555716353119, 0, 333, 0.0, 1.0, 1.0, 3.0, 3.4187611320007916, 0.0, 0.0], "isController": false}, {"data": ["CART_GET - verify update", 2727, 0, 0.0, 1.6769343601026756, 0, 15, 1.0, 3.0, 4.0, 6.0, 3.4188184202476295, 9.776293626135217, 1.0542644768530822], "isController": false}, {"data": ["AUTH - login", 2757, 0, 0.0, 2.6463547334058757, 0, 22, 2.0, 4.0, 5.0, 9.0, 3.422663569675474, 2.214895294210025, 1.3354807064721488], "isController": false}, {"data": ["READ - search products", 2750, 0, 0.0, 1.9709090909090925, 0, 15, 2.0, 4.0, 4.0, 7.0, 3.419998159419172, 1.5129484045086767, 1.1681795559660935], "isController": false}, {"data": ["POST_CHECKOUT_CART - expected empty", 2700, 2700, 100.0, 1.651851851851853, 0, 17, 1.0, 3.0, 4.0, 7.0, 3.4130296832455636, 9.676198388196731, 1.0524742648081244], "isController": false}]}, function(index, item){
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
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": [{"data": ["Known business gap: cart not empty after checkout", 2700, 100.0, 10.972041612483745], "isController": false}]}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 24608, 2700, "Known business gap: cart not empty after checkout", 2700, "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": ["POST_CHECKOUT_CART - expected empty", 2700, 2700, "Known business gap: cart not empty after checkout", 2700, "", "", "", "", "", "", "", ""], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
