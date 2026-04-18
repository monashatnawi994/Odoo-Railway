FROM odoo:17

USER root
WORKDIR /opt/odoo/src

# Copy source code so custom core changes are included in the deployment.
COPY . /opt/odoo/src

# Railway runtime configuration and startup script.
COPY ./setup/odoo-railway.conf /etc/odoo/odoo.conf
RUN chmod +x /opt/odoo/src/setup/railway-start.sh \
    && chown -R odoo:odoo /opt/odoo/src /etc/odoo/odoo.conf

USER odoo

CMD ["/opt/odoo/src/setup/railway-start.sh"]
