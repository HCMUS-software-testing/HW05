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

    var data = {"OkPercent": 100.0, "KoPercent": 0.0};
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
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [1.0, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/180)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/160)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/192)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/184)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/172)"], "isController": false}, {"data": [1.0, 500, 1500, "2. Read - Get Admin Users (GET /api/admin/users)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/197)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/185)"], "isController": false}, {"data": [1.0, 500, 1500, "5. Transactional - Create Product (POST /api/products)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/177)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/165)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/157)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/189)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/169)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/202)"], "isController": false}, {"data": [1.0, 500, 1500, "1. Auth - Admin Login (POST /api/login)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/193)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/181)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/173)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/161)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/186)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/174)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/166)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/198)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/178)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/203)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/158)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/190)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/182)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/170)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/162)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/194)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/204)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/175)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/163)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/199)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/187)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/179)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/167)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/200)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/159)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/191)"], "isController": false}, {"data": [1.0, 500, 1500, "3. Read - Get Products List (GET /api/products)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/171)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/195)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/183)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/205)"], "isController": false}, {"data": [1.0, 500, 1500, "4. Read - Get Categories (GET /api/categories)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/164)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/196)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/188)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/176)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/168)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/201)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/156)"], "isController": false}]}, function(index, item){
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
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 300, 0, 0.0, 9.846666666666666, 3, 42, 8.0, 17.0, 17.0, 19.0, 4.407422098814403, 2.4676685747131506, 0.9983557101826143], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/180)", 1, 0, 0.0, 13.0, 13, 13, 13.0, 13.0, 13.0, 13.0, 76.92307692307693, 20.13221153846154, 13.596754807692308], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/160)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 11.04736328125], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/192)", 1, 0, 0.0, 19.0, 19, 19, 19.0, 19.0, 19.0, 19.0, 52.63157894736842, 13.774671052631579, 9.303042763157896], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/184)", 1, 0, 0.0, 15.0, 15, 15, 15.0, 15.0, 15.0, 15.0, 66.66666666666667, 17.447916666666668, 11.783854166666668], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/172)", 1, 0, 0.0, 19.0, 19, 19, 19.0, 19.0, 19.0, 19.0, 52.63157894736842, 13.774671052631579, 9.303042763157896], "isController": false}, {"data": ["2. Read - Get Admin Users (GET /api/admin/users)", 50, 0, 0.0, 6.84, 3, 10, 7.0, 9.0, 9.449999999999996, 10.0, 0.8359806052499582, 0.4122755914562782, 0.25879477721116867], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/197)", 1, 0, 0.0, 18.0, 18, 18, 18.0, 18.0, 18.0, 18.0, 55.55555555555555, 14.539930555555557, 9.819878472222223], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/185)", 1, 0, 0.0, 18.0, 18, 18, 18.0, 18.0, 18.0, 18.0, 55.55555555555555, 14.539930555555557, 9.819878472222223], "isController": false}, {"data": ["5. Transactional - Create Product (POST /api/products)", 50, 0, 0.0, 15.96, 11, 41, 16.0, 18.0, 19.0, 41.0, 0.7820320320320321, 0.21154577428991492, 0.27166448675237737], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/177)", 1, 0, 0.0, 17.0, 17, 17, 17.0, 17.0, 17.0, 17.0, 58.8235294117647, 15.395220588235293, 10.39751838235294], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/165)", 1, 0, 0.0, 13.0, 13, 13, 13.0, 13.0, 13.0, 13.0, 76.92307692307693, 20.13221153846154, 13.596754807692308], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/157)", 1, 0, 0.0, 17.0, 17, 17, 17.0, 17.0, 17.0, 17.0, 58.8235294117647, 15.395220588235293, 10.39751838235294], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/189)", 1, 0, 0.0, 17.0, 17, 17, 17.0, 17.0, 17.0, 17.0, 58.8235294117647, 15.395220588235293, 10.39751838235294], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/169)", 1, 0, 0.0, 14.0, 14, 14, 14.0, 14.0, 14.0, 14.0, 71.42857142857143, 18.694196428571427, 12.625558035714285], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/202)", 1, 0, 0.0, 13.0, 13, 13, 13.0, 13.0, 13.0, 13.0, 76.92307692307693, 20.13221153846154, 13.596754807692308], "isController": false}, {"data": ["1. Auth - Admin Login (POST /api/login)", 50, 0, 0.0, 8.440000000000005, 4, 42, 8.0, 10.0, 11.449999999999996, 42.0, 0.8281299170213823, 0.4949370207198105, 0.18277086059260977], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/193)", 1, 0, 0.0, 14.0, 14, 14, 14.0, 14.0, 14.0, 14.0, 71.42857142857143, 18.694196428571427, 12.625558035714285], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/181)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 11.04736328125], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/173)", 1, 0, 0.0, 13.0, 13, 13, 13.0, 13.0, 13.0, 13.0, 76.92307692307693, 20.13221153846154, 13.596754807692308], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/161)", 1, 0, 0.0, 17.0, 17, 17, 17.0, 17.0, 17.0, 17.0, 58.8235294117647, 15.395220588235293, 10.39751838235294], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/186)", 1, 0, 0.0, 17.0, 17, 17, 17.0, 17.0, 17.0, 17.0, 58.8235294117647, 15.395220588235293, 10.39751838235294], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/174)", 1, 0, 0.0, 15.0, 15, 15, 15.0, 15.0, 15.0, 15.0, 66.66666666666667, 17.447916666666668, 11.783854166666668], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/166)", 1, 0, 0.0, 17.0, 17, 17, 17.0, 17.0, 17.0, 17.0, 58.8235294117647, 15.395220588235293, 10.39751838235294], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/198)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 11.04736328125], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/178)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 11.04736328125], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/203)", 1, 0, 0.0, 15.0, 15, 15, 15.0, 15.0, 15.0, 15.0, 66.66666666666667, 17.447916666666668, 11.783854166666668], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/158)", 1, 0, 0.0, 17.0, 17, 17, 17.0, 17.0, 17.0, 17.0, 58.8235294117647, 15.395220588235293, 10.39751838235294], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/190)", 1, 0, 0.0, 13.0, 13, 13, 13.0, 13.0, 13.0, 13.0, 76.92307692307693, 20.13221153846154, 13.596754807692308], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/182)", 1, 0, 0.0, 17.0, 17, 17, 17.0, 17.0, 17.0, 17.0, 58.8235294117647, 15.395220588235293, 10.39751838235294], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/170)", 1, 0, 0.0, 15.0, 15, 15, 15.0, 15.0, 15.0, 15.0, 66.66666666666667, 17.447916666666668, 11.783854166666668], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/162)", 1, 0, 0.0, 12.0, 12, 12, 12.0, 12.0, 12.0, 12.0, 83.33333333333333, 21.809895833333332, 14.729817708333332], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/194)", 1, 0, 0.0, 17.0, 17, 17, 17.0, 17.0, 17.0, 17.0, 58.8235294117647, 15.395220588235293, 10.39751838235294], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/204)", 1, 0, 0.0, 18.0, 18, 18, 18.0, 18.0, 18.0, 18.0, 55.55555555555555, 14.539930555555557, 9.819878472222223], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/175)", 1, 0, 0.0, 19.0, 19, 19, 19.0, 19.0, 19.0, 19.0, 52.63157894736842, 13.774671052631579, 9.303042763157896], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/163)", 1, 0, 0.0, 15.0, 15, 15, 15.0, 15.0, 15.0, 15.0, 66.66666666666667, 17.447916666666668, 11.783854166666668], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/199)", 1, 0, 0.0, 12.0, 12, 12, 12.0, 12.0, 12.0, 12.0, 83.33333333333333, 21.809895833333332, 14.729817708333332], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/187)", 1, 0, 0.0, 17.0, 17, 17, 17.0, 17.0, 17.0, 17.0, 58.8235294117647, 15.395220588235293, 10.39751838235294], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/179)", 1, 0, 0.0, 13.0, 13, 13, 13.0, 13.0, 13.0, 13.0, 76.92307692307693, 20.13221153846154, 13.596754807692308], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/167)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 11.04736328125], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/200)", 1, 0, 0.0, 15.0, 15, 15, 15.0, 15.0, 15.0, 15.0, 66.66666666666667, 17.447916666666668, 11.783854166666668], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/159)", 1, 0, 0.0, 15.0, 15, 15, 15.0, 15.0, 15.0, 15.0, 66.66666666666667, 17.447916666666668, 11.783854166666668], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/191)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 11.04736328125], "isController": false}, {"data": ["3. Read - Get Products List (GET /api/products)", 50, 0, 0.0, 6.080000000000001, 4, 10, 6.0, 7.899999999999999, 8.0, 10.0, 0.8073370793773816, 1.1415935522024154, 0.1222043430698185], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/171)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 11.04736328125], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/195)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 11.04736328125], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/183)", 1, 0, 0.0, 13.0, 13, 13, 13.0, 13.0, 13.0, 13.0, 76.92307692307693, 20.13221153846154, 13.596754807692308], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/205)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 11.04736328125], "isController": false}, {"data": ["4. Read - Get Categories (GET /api/categories)", 50, 0, 0.0, 6.039999999999998, 3, 14, 6.0, 7.0, 8.899999999999991, 14.0, 0.8261458643138033, 0.266238413304253, 0.1266649420871749], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/164)", 1, 0, 0.0, 14.0, 14, 14, 14.0, 14.0, 14.0, 14.0, 71.42857142857143, 18.694196428571427, 12.625558035714285], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/196)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 11.04736328125], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/188)", 1, 0, 0.0, 17.0, 17, 17, 17.0, 17.0, 17.0, 17.0, 58.8235294117647, 15.395220588235293, 10.39751838235294], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/176)", 1, 0, 0.0, 17.0, 17, 17, 17.0, 17.0, 17.0, 17.0, 58.8235294117647, 15.395220588235293, 10.39751838235294], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/168)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 11.04736328125], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/201)", 1, 0, 0.0, 15.0, 15, 15, 15.0, 15.0, 15.0, 15.0, 66.66666666666667, 17.447916666666668, 11.783854166666668], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/156)", 1, 0, 0.0, 18.0, 18, 18, 18.0, 18.0, 18.0, 18.0, 55.55555555555555, 14.539930555555557, 9.819878472222223], "isController": false}]}, function(index, item){
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
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": []}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 300, 0, "", "", "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
