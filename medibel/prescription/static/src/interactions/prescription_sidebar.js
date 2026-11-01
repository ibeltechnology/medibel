import { Sidebar } from "@portal/interactions/sidebar";
import { registry } from "@web/core/registry";
import { scrollTo } from "@web/core/utils/scrolling";

const PAGE_WIDTH = 1040;
const PAGE_HEIGHT = 1464;

export class PrescriptionSidebar extends Sidebar {
    static selector = ".o_portal_prescription_sidebar";

    dynamicContent = {
        _window: {
            "t-on-resize": this.updateIframeSize,
        },
    };

    setup() {
        super.setup();
        this.prescriptionHTMLEl = undefined;
    }

    start() {
        super.start();

        this.prescriptionHTMLEl = this.el.querySelector(
            "#prescription_html"
        );

        if (!this.prescriptionHTMLEl) {
            return;
        }

        // Écouter le chargement du rapport.
        this.addListener(
            this.prescriptionHTMLEl,
            "load",
            this.onIframeLoad
        );

        const iframeDoc =
            this.prescriptionHTMLEl.contentDocument;

        if (iframeDoc?.readyState === "complete") {
            this.onIframeLoad();
        }
    }

    onIframeLoad() {
        const iframeDoc =
            this.prescriptionHTMLEl?.contentDocument;

        if (!iframeDoc) {
            return;
        }

        // Reprendre la présentation des rapports Odoo.
        const mainEl = iframeDoc.querySelector("main");

        if (mainEl) {
            mainEl.classList.add(
                "d-flex",
                "flex-column",
                "min-vh-100"
            );
        }

        this.updateIframeSize();
    }

    updateIframeSize() {
        if (!this.prescriptionHTMLEl) {
            return;
        }

        const iframeDoc =
            this.prescriptionHTMLEl.contentDocument;

        const wrapwrapEl =
            iframeDoc?.querySelector("div#wrapwrap");

        if (!wrapwrapEl) {
            return;
        }

        const iframe = this.prescriptionHTMLEl;
        const container = iframe.parentElement;

        if (!container) {
            return;
        }

        // Dimensions de référence du rapport.
        iframe.width = PAGE_WIDTH;
        iframe.height = 0;

        const height = Math.max(
            wrapwrapEl.scrollHeight,
            PAGE_HEIGHT
        );

        const scale =
            container.clientWidth / PAGE_WIDTH;

        iframe.height = height;

        // Réduction proportionnelle du rapport.
        iframe.style.transformOrigin = "top left";
        iframe.style.transform = `scale(${scale})`;

        // Adapter la hauteur du conteneur.
        container.style.height = `${height * scale}px`;

        // Gestion des ancres.
        const isAnchor = /^#[\w-]+$/.test(
            window.location.hash
        );

        if (!isAnchor) {
            return;
        }

        const targetEl = document.querySelector(
            window.location.hash
        );

        if (targetEl) {
            scrollTo(targetEl, {
                behavior: "instant",
            });
        }
    }
}

registry
    .category("public.interactions")
    .add(
        "prescription.prescription_sidebar",
        PrescriptionSidebar
    );
