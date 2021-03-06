// TODO:
// - add details data for all languages
// - add button to the docs
import debounce from "../libs/debounce";

function initFSFLanguageSelect(rootEl) {
  const flowLinks = [].slice.call(rootEl.querySelectorAll(".p-flow-link"));
  const flowDetails = [].slice.call(rootEl.querySelectorAll(".p-flow-details"));

  const closeDetails = () => {
    flowDetails.forEach(e => (e.style.display = "none"));
    flowLinks.forEach(l => l.classList.remove("is-open"));
    window.location.hash = "";
  };

  const openDetails = link => {
    if (link && link.dataset.flowLink) {
      // find where the next row of links starts to insert details panel before
      var top = link.offsetTop;

      var nextRow = null;
      for (
        var i = flowLinks.indexOf(link);
        i < flowLinks.length && !nextRow;
        i++
      ) {
        if (flowLinks[i].offsetTop > top) {
          nextRow = flowLinks[i];
        }
      }
      const isOpen = link.classList.contains("is-open");

      closeDetails();

      if (!isOpen) {
        // find the end of the row of icons to place details panel properly
        var details = rootEl.querySelector(
          `[data-flow-details='${link.dataset.flowLink}'`
        );
        if (nextRow) {
          nextRow.parentNode.insertBefore(details, nextRow);
        } else {
          rootEl.appendChild(details);
        }
        details.style.display = "block";
        link.classList.add("is-open");
        window.location.hash = link.dataset.flowLink;
      } else {
        link.classList.remove("is-open");
        window.location.hash = "";
      }

      window.scrollTo(0, link.offsetTop);
    }
  };

  rootEl.addEventListener("click", event => {
    var link = event.target.closest(".p-flow-link");

    if (link) {
      openDetails(link);
      event.preventDefault();
    }
  });

  // if there is a hash in URL that corresponds to one of the languages
  // open given language section (for example /first-snap#python)
  const hash = window.location.hash.slice(1);
  const link = rootEl.querySelector(`[data-flow-link='${hash}'`);
  if (link) {
    openDetails(link);
  }

  const onResize = debounce(closeDetails, 500);
  window.addEventListener("resize", onResize);
}

export { initFSFLanguageSelect };
