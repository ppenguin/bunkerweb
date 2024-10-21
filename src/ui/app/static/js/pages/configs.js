$(document).ready(function () {
  var actionLock = false;
  const configNumber = parseInt($("#configs_number").val());
  const services = $("#services").val().trim().split(" ");
  const templates = $("#templates").val().trim().split(" ");
  const configServiceSelection = $("#configs_service_selection").val().trim();
  const configTypeSelection = $("#configs_type_selection")
    .val()
    .trim()
    .toUpperCase();
  const isReadOnly = $("#is-read-only").val().trim() === "True";

  const servicesSearchPanesOptions = [
    {
      label: "global",
      value: function (rowData) {
        return $(rowData[4]).text().trim() === "global";
      },
    },
  ];
  const templatesSearchPanesOptions = [
    {
      label: "no template",
      value: function (rowData) {
        return $(rowData[5]).text().trim() === "no template";
      },
    },
  ];

  services.forEach((service) => {
    servicesSearchPanesOptions.push({
      label: service,
      value: function (rowData) {
        return $(rowData[4]).text().trim() === service;
      },
    });
  });
  templates.forEach((template) => {
    templatesSearchPanesOptions.push({
      label: template,
      value: function (rowData) {
        return $(rowData[5]).text().trim() === template;
      },
    });
  });

  const setupDeletionModal = (configs) => {
    const delete_modal = $("#modal-delete-configs");
    const list = $(
      `<ul class="list-group list-group-horizontal d-flex w-100">
      <li class="list-group-item align-items-center text-center bg-secondary text-white" style="flex: 1 1 0;">
        <div class="ms-2 me-auto">
          <div class="fw-bold">Name</div>
        </div>
      </li>
      <li class="list-group-item align-items-center text-center bg-secondary text-white" style="flex: 1 1 0;">
        <div class="fw-bold">Type</div>
      </li>
      <li class="list-group-item align-items-center text-center bg-secondary text-white" style="flex: 1 1 0;">
        <div class="fw-bold">Service</div>
      </li>
      </ul>`,
    );
    $("#selected-configs-delete").append(list);

    configs.forEach((config) => {
      const list = $(
        `<ul class="list-group list-group-horizontal d-flex w-100"></ul>`,
      );

      // Create the list item using template literals
      const listItem =
        $(`<li class="list-group-item align-items-center" style="flex: 1 1 0;">
  <div class="ms-2 me-auto">
    <div class="fw-bold">${config.name}</div>
  </div>
</li>`);
      list.append(listItem);

      const id = `${config.type.toLowerCase()}-${config.service.replaceAll(
        ".",
        "_",
      )}-${config.name}`;

      // Clone the type element and append it to the list item
      const typeClone = $(`#type-${id}`).clone();
      const typeListItem = $(
        `<li class="list-group-item d-flex align-items-center" style="flex: 1 1 0;"></li>`,
      );
      typeListItem.append(typeClone.removeClass("highlight"));
      list.append(typeListItem);

      // Clone the service element and append it to the list item
      const serviceClone = $(`#service-${id}`).clone();
      const serviceListItem = $(
        `<li class="list-group-item d-flex align-items-center" style="flex: 1 1 0;"></li>`,
      );
      serviceListItem.append(serviceClone.removeClass("highlight"));
      list.append(serviceListItem);
      serviceClone.find('[data-bs-toggle="tooltip"]').tooltip();

      $("#selected-configs-delete").append(list);
    });

    const modal = new bootstrap.Modal(delete_modal);
    delete_modal
      .find(".alert")
      .text(
        `Are you sure you want to delete the selected custom configuration${"s".repeat(
          configs.length > 1,
        )}?`,
      );
    modal.show();

    configs.forEach((config) => {
      if (config.service === "global") {
        config.service = null;
      }
    });
    $("#selected-configs-input-delete").val(JSON.stringify(configs));
  };

  const layout = {
    topStart: {},
    bottomEnd: {},
    bottom1: {
      searchPanes: {
        viewTotal: true,
        cascadePanes: true,
        columns: [2, 3, 4, 5],
      },
    },
  };

  if (configNumber > 10) {
    const menu = [10];
    if (configNumber > 25) {
      menu.push(25);
    }
    if (configNumber > 50) {
      menu.push(50);
    }
    if (configNumber > 100) {
      menu.push(100);
    }
    menu.push({ label: "All", value: -1 });
    layout.topStart.pageLength = {
      menu: menu,
    };
    layout.bottomEnd.paging = true;
  }

  layout.topStart.buttons = [
    {
      extend: "create_config",
    },
    {
      extend: "colvis",
      columns: "th:not(:first-child):not(:nth-child(2)):not(:last-child)",
      text: '<span class="tf-icons bx bx-columns bx-18px me-2"></span>Columns',
      className: "btn btn-sm btn-outline-primary",
      columnText: function (dt, idx, title) {
        return idx + 1 + ". " + title;
      },
    },
    {
      extend: "colvisRestore",
      text: '<span class="tf-icons bx bx-reset bx-18px me-2"></span>Reset<span class="d-none d-md-inline"> columns</span>',
      className: "btn btn-sm btn-outline-primary",
    },
    {
      extend: "collection",
      text: '<span class="tf-icons bx bx-export bx-18px me-2"></span>Export',
      className: "btn btn-sm btn-outline-primary",
      buttons: [
        {
          extend: "copy",
          text: '<span class="tf-icons bx bx-copy bx-18px me-2"></span>Copy visible',
          exportOptions: {
            columns: ":visible:not(:first-child):not(:last-child)",
          },
        },
        {
          extend: "csv",
          text: '<span class="tf-icons bx bx-table bx-18px me-2"></span>CSV',
          bom: true,
          filename: "bw_custom_configs",
          exportOptions: {
            modifier: {
              search: "none",
            },
            columns: ":not(:first-child):not(:last-child)",
          },
        },
        {
          extend: "excel",
          text: '<span class="tf-icons bx bx-table bx-18px me-2"></span>Excel',
          filename: "bw_custom_configs",
          exportOptions: {
            modifier: {
              search: "none",
            },
            columns: ":not(:first-child):not(:last-child)",
          },
        },
      ],
    },
    {
      extend: "collection",
      text: '<span class="tf-icons bx bx-play bx-18px me-2"></span>Actions',
      className: "btn btn-sm btn-outline-primary",
      buttons: [
        {
          extend: "delete_configs",
          className: "text-danger",
        },
      ],
    },
  ];

  $(document).on("hidden.bs.toast", ".toast", function (event) {
    if (event.target.id.startsWith("feedback-toast")) {
      setTimeout(() => {
        $(this).remove();
      }, 100);
    }
  });

  $("#modal-delete-configs").on("hidden.bs.modal", function () {
    $("#selected-configs-delete").empty();
    $("#selected-configs-input-delete").val("");
  });

  const getSelectedConfigs = () => {
    const configs = [];
    $("tr.selected").each(function () {
      const $this = $(this);
      const name = $this.find("td:eq(1)").find("a").text().trim();
      const type = $this.find("td:eq(2)").text().trim();
      let service = $this.find("td:eq(4)");
      if (service.find("a").length > 0) {
        service = service.find("a").text().trim();
      } else {
        service = service.text().trim();
      }
      configs.push({ name: name, type: type, service: service });
    });
    return configs;
  };

  $.fn.dataTable.ext.buttons.create_config = {
    text: '<span class="tf-icons bx bx-plus"></span>&nbsp;Create<span class="d-none d-md-inline"> new custom config</span>',
    className: `btn btn-sm btn-outline-bw-green${
      isReadOnly ? " disabled" : ""
    }`,
    action: function (e, dt, node, config) {
      if (isReadOnly) {
        alert("This action is not allowed in read-only mode.");
        return;
      }
      window.location.href = `${window.location.href}/new`;
    },
  };

  $.fn.dataTable.ext.buttons.delete_configs = {
    text: '<span class="tf-icons bx bx-trash bx-18px me-2"></span>Delete',
    action: function (e, dt, node, config) {
      if (isReadOnly) {
        alert("This action is not allowed in read-only mode.");
        return;
      }
      if (actionLock) {
        return;
      }
      actionLock = true;
      $(".dt-button-background").click();

      const configs = getSelectedConfigs();
      if (configs.length === 0) {
        actionLock = false;
        return;
      }

      setupDeletionModal(configs);

      actionLock = false;
    },
  };

  const configs_table = new DataTable("#configs", {
    columnDefs: [
      {
        orderable: false,
        render: DataTable.render.select(),
        targets: 0,
      },
      {
        orderable: false,
        targets: -1,
      },
      {
        visible: false,
        targets: 6,
      },
      {
        searchPanes: {
          show: true,
          options: [
            {
              label: '<i class="bx bx-xs bx-window-alt"></i>&nbsp;HTTP',
              value: function (rowData, rowIdx) {
                return / HTTP$/.test(rowData[2].trim());
              },
            },
            {
              label: '<i class="bx bx-xs bx-window-alt"></i>&nbsp;SERVER_HTTP',
              value: function (rowData, rowIdx) {
                return / SERVER_HTTP$/.test(rowData[2].trim());
              },
            },
            {
              label:
                '<i class="bx bx-xs bx-window-alt"></i>&nbsp;DEFAULT_SERVER_HTTP',
              value: function (rowData, rowIdx) {
                return / DEFAULT_SERVER_HTTP$/.test(rowData[2].trim());
              },
            },
            {
              label:
                '<i class="bx bx-xs bx-shield-quarter"></i>&nbsp;MODSEC_CRS',
              value: function (rowData, rowIdx) {
                return / MODSEC_CRS$/.test(rowData[2].trim());
              },
            },
            {
              label: '<i class="bx bx-xs bx-shield-alt-2"></i>&nbsp;MODSEC',
              value: function (rowData, rowIdx) {
                return / MODSEC$/.test(rowData[2].trim());
              },
            },
            {
              label: '<i class="bx bx-xs bx-network-chart"></i>&nbsp;STREAM',
              value: function (rowData, rowIdx) {
                return / STREAM$/.test(rowData[2].trim());
              },
            },
            {
              label:
                '<i class="bx bx-xs bx-network-chart"></i>&nbsp;SERVER_STREAM',
              value: function (rowData, rowIdx) {
                return / SERVER_STREAM$/.test(rowData[2].trim());
              },
            },
            {
              label:
                '<i class="bx bx-xs bx-shield-alt"></i>&nbsp;CRS_PLUGINS_BEFORE',
              value: function (rowData, rowIdx) {
                return rowData[2].includes("BEFORE");
              },
            },
            {
              label:
                '<i class="bx bx-xs bx-shield-alt"></i>&nbsp;CRS_PLUGINS_AFTER',
              value: function (rowData, rowIdx) {
                return rowData[2].includes("AFTER");
              },
            },
          ],
          combiner: "or",
        },
        targets: 2,
      },
      {
        searchPanes: {
          show: true,
          combiner: "or",
          options: servicesSearchPanesOptions,
        },
        targets: 4,
      },
      {
        searchPanes: {
          show: true,
          combiner: "or",
          orderable: false,
        },
        targets: 3,
      },
      {
        searchPanes: {
          show: true,
          combiner: "or",
          options: templatesSearchPanesOptions,
        },
        targets: 5,
      },
      {
        targets: "_all", // Target all columns
        createdCell: function (td, cellData, rowData, row, col) {
          $(td).addClass("align-items-center"); // Apply 'text-center' class to <td>
        },
      },
    ],
    order: [[1, "asc"]],
    autoFill: false,
    responsive: true,
    select: {
      style: "multi+shift",
      selector: "td:first-child",
      headerCheckbox: false,
    },
    layout: layout,
    language: {
      info: "Showing _START_ to _END_ of _TOTAL_ custom configs",
      infoEmpty: "No custom configs available",
      infoFiltered: "(filtered from _MAX_ total custom configs)",
      lengthMenu: "Display _MENU_ custom configs",
      zeroRecords: "No matching custom configs found",
      select: {
        rows: {
          _: "Selected %d custom configs",
          0: "No custom configs selected",
          1: "Selected 1 custom config",
        },
      },
    },
    initComplete: function (settings, json) {
      $("#configs_wrapper .btn-secondary").removeClass("btn-secondary");
      $("#configs_wrapper th").addClass("text-center");
      if (isReadOnly)
        $("#configs_wrapper .dt-buttons")
          .attr(
            "data-bs-original-title",
            "The database is in readonly, therefore you cannot create new custom configurations.",
          )
          .attr("data-bs-placement", "right")
          .tooltip();
    },
  });

  $(`#DataTables_Table_0 span[title='${configTypeSelection}']`).trigger(
    "click",
  );

  $(`#DataTables_Table_2 span[title='${configServiceSelection}']`).trigger(
    "click",
  );

  $("#configs").removeClass("d-none");
  $("#configs-waiting").addClass("visually-hidden");

  configs_table.on("mouseenter", "td", function () {
    if (configs_table.cell(this).index() === undefined) return;
    const rowIdx = configs_table.cell(this).index().row;

    configs_table
      .cells()
      .nodes()
      .each((el) => el.classList.remove("highlight"));

    configs_table
      .cells()
      .nodes()
      .each(function (el) {
        if (configs_table.cell(el).index().row === rowIdx)
          el.classList.add("highlight");
      });
  });

  configs_table.on("mouseleave", "td", function () {
    configs_table
      .cells()
      .nodes()
      .each((el) => el.classList.remove("highlight"));
  });

  // Event listener for the select-all checkbox
  $("#select-all-rows").on("change", function () {
    const isChecked = $(this).prop("checked");

    if (isChecked) {
      // Select all rows on the current page
      configs_table.rows({ page: "current" }).select();
    } else {
      // Deselect all rows on the current page
      configs_table.rows({ page: "current" }).deselect();
    }
  });

  $(document).on("click", ".delete-config", function () {
    if (isReadOnly) {
      alert("This action is not allowed in read-only mode.");
      return;
    }
    const config = {
      name: $(this).data("config-name"),
      type: $(this).data("config-type"),
      service: $(this).data("config-service"),
    };
    setupDeletionModal([config]);
  });
});