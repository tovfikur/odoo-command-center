# Developer Terminal - Usage Examples

This document provides practical examples for using the Developer Terminal module.

## Table of Contents
1. [Shell Commands](#shell-commands)
2. [Python Code](#python-code)
3. [Package Management](#package-management)
4. [Odoo-Specific Tasks](#odoo-specific-tasks)
5. [Advanced Examples](#advanced-examples)

---

## Shell Commands

### Basic System Information

```bash
# Check current user
whoami

# Check current directory
pwd

# List files in current directory
ls -la

# Check Python version
python --version

# Check disk space
df -h

# Check memory usage
free -m

# Check system information
uname -a

# Find Python executable
which python
```

### File Operations

```bash
# List Python files
find . -name "*.py" | head -n 20

# Search for a string in files
grep -r "def execute" . --include="*.py" | head -n 10

# Count Python files
find . -name "*.py" | wc -l

# Show file contents
cat /etc/odoo/odoo.conf

# Display first 10 lines
head -n 10 /var/log/odoo/odoo.log

# Display last 20 lines
tail -n 20 /var/log/odoo/odoo.log
```

### Package and Dependency Management

```bash
# List installed Python packages
pip list

# Show specific package info
pip show odoo

# Check for outdated packages
pip list --outdated

# Search for a package
pip search requests

# Show package dependencies
pip show -f werkzeug
```

### Process and Network

```bash
# List running processes
ps aux | grep odoo

# Check open ports
netstat -tuln

# Check network connectivity
ping -c 4 google.com

# DNS lookup
nslookup google.com

# Check environment variables
env | grep -i python
```

---

## Python Code

### Basic Odoo Operations

```python
# Get current user information
user = env.user
print(f"User: {user.name}")
print(f"Login: {user.login}")
print(f"Email: {user.email}")
print(f"Groups: {[g.name for g in user.groups_id]}")

# Get database name
print(f"Database: {env.cr.dbname}")

# Check Odoo version
print(f"Odoo Version: {env['ir.module.module'].get_odoo_version()}")

# List all companies
companies = env['res.company'].search([])
for company in companies:
    print(f"Company: {company.name} - Currency: {company.currency_id.name}")
```

### Working with Partners

```python
# Count total partners
total = env['res.partner'].search_count([])
print(f"Total partners: {total}")

# List recent partners
partners = env['res.partner'].search([], limit=10, order='create_date desc')
for p in partners:
    print(f"ID: {p.id:5d} | Name: {p.name:30s} | Email: {p.email or 'N/A'}")

# Find partners by country
us_partners = env['res.partner'].search([('country_id.code', '=', 'US')], limit=5)
print(f"Found {len(us_partners)} US partners:")
for p in us_partners:
    print(f"  - {p.name} ({p.city}, {p.state_id.name})")

# Create a test partner
new_partner = env['res.partner'].create({
    'name': 'Test Partner from Terminal',
    'email': 'test@terminal.com',
    'phone': '+1234567890',
})
print(f"Created partner ID: {new_partner.id}")
```

### Working with Users

```python
# List all active users
users = env['res.users'].search([('active', '=', True)])
print(f"Active users: {len(users)}")
for user in users:
    print(f"  - {user.name} ({user.login})")

# Find administrators
admins = env['res.users'].search([('groups_id', 'in', env.ref('base.group_system').id)])
print(f"\nSystem Administrators:")
for admin in admins:
    print(f"  - {admin.name}")

# Check user permissions
user = env.user
has_sales = user.has_group('sales_team.group_sale_salesman')
has_settings = user.has_group('base.group_system')
print(f"Has Sales permissions: {has_sales}")
print(f"Has Settings permissions: {has_settings}")
```

### Working with Models

```python
# List all installed modules
modules = env['ir.module.module'].search([('state', '=', 'installed')])
print(f"Installed modules: {len(modules)}")
for mod in modules[:10]:
    print(f"  - {mod.name}: {mod.shortdesc}")

# Get model information
model = env['ir.model'].search([('model', '=', 'res.partner')], limit=1)
print(f"\nModel: {model.name}")
print(f"Table: {model.model}")
print(f"Fields count: {len(model.field_id)}")

# List model fields
for field in model.field_id[:10]:
    print(f"  - {field.name} ({field.ttype})")
```

### Database Operations

```python
# Execute SQL query (read-only)
env.cr.execute("SELECT COUNT(*) FROM res_partner")
count = env.cr.fetchone()[0]
print(f"Partners (via SQL): {count}")

# Get table sizes
env.cr.execute("""
    SELECT
        schemaname,
        tablename,
        pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
    FROM pg_tables
    WHERE schemaname = 'public'
    ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
    LIMIT 10
""")
print("\nLargest tables:")
for schema, table, size in env.cr.fetchall():
    print(f"  {table:30s} - {size}")

# Count records by model
models = ['res.partner', 'res.users', 'ir.model', 'ir.ui.view']
for model_name in models:
    count = env[model_name].search_count([])
    print(f"{model_name:20s}: {count:6d} records")
```

### Date and Time Operations

```python
from datetime import datetime, timedelta

# Current date and time
now = datetime.now()
print(f"Current time: {now}")
print(f"ISO format: {now.isoformat()}")

# Date calculations
yesterday = now - timedelta(days=1)
next_week = now + timedelta(weeks=1)
print(f"Yesterday: {yesterday.date()}")
print(f"Next week: {next_week.date()}")

# Find records created today
today_start = now.replace(hour=0, minute=0, second=0)
partners_today = env['res.partner'].search([
    ('create_date', '>=', today_start)
])
print(f"\nPartners created today: {len(partners_today)}")

# Find records created this month
month_start = now.replace(day=1, hour=0, minute=0, second=0)
partners_this_month = env['res.partner'].search([
    ('create_date', '>=', month_start)
])
print(f"Partners created this month: {len(partners_this_month)}")
```

---

## Package Management

### Installing Common Packages

```bash
# Web scraping
requests
beautifulsoup4
lxml

# Data analysis
pandas
numpy
scipy

# Image processing
pillow
opencv-python

# PDF handling
pypdf2
reportlab

# Excel files
openpyxl
xlrd
xlsxwriter

# HTTP client
httpx

# JSON/YAML
pyyaml

# Date/time utilities
python-dateutil

# Cryptography
cryptography

# Testing
pytest
```

### Package Management Commands

Via Terminal (Shell):
```bash
# Install package
pip install requests

# Install specific version
pip install requests==2.28.0

# Install from requirements file
pip install -r requirements.txt

# Upgrade package
pip install --upgrade requests

# Uninstall package
pip uninstall -y requests

# Show package details
pip show requests

# List outdated packages
pip list --outdated

# Freeze current packages
pip freeze > requirements.txt
```

---

## Odoo-Specific Tasks

### Module Management

```python
# List installed modules
installed = env['ir.module.module'].search([('state', '=', 'installed')])
print(f"Installed modules: {len(installed)}")
for mod in installed[:20]:
    print(f"  - {mod.name}: {mod.shortdesc}")

# Find modules to upgrade
to_upgrade = env['ir.module.module'].search([('state', '=', 'to upgrade')])
print(f"\nModules to upgrade: {len(to_upgrade)}")

# Get module dependencies
module = env['ir.module.module'].search([('name', '=', 'sale')], limit=1)
if module:
    print(f"\n{module.shortdesc} dependencies:")
    for dep in module.dependencies_id:
        print(f"  - {dep.name}")
```

### Configuration and Settings

```python
# Get configuration parameters
ICP = env['ir.config_parameter'].sudo()

# List all config parameters
params = ICP.search([])
print(f"Configuration parameters: {len(params)}")
for param in params[:10]:
    print(f"  {param.key} = {param.value}")

# Get specific parameter
web_base_url = ICP.get_param('web.base.url')
print(f"\nBase URL: {web_base_url}")

# Set a parameter (be careful!)
# ICP.set_param('my.custom.param', 'value')
```

### Workflow and Automation

```python
# Find scheduled actions (cron jobs)
crons = env['ir.cron'].search([])
print(f"Scheduled actions: {len(crons)}")
for cron in crons[:10]:
    print(f"  - {cron.name}")
    print(f"    Model: {cron.model_id.model}")
    print(f"    Interval: {cron.interval_number} {cron.interval_type}")
    print(f"    Active: {cron.active}")
    print()

# Check for active automation rules
automations = env['base.automation'].search([('active', '=', True)])
print(f"Active automation rules: {len(automations)}")
```

### Email and Communication

```python
# Check email configuration
mail_servers = env['ir.mail_server'].search([])
print(f"Mail servers configured: {len(mail_servers)}")
for server in mail_servers:
    print(f"  - {server.name}: {server.smtp_host}:{server.smtp_port}")

# Count email messages
messages = env['mail.message'].search_count([])
print(f"\nTotal messages: {messages}")

# Recent messages
recent = env['mail.message'].search([], limit=5, order='date desc')
for msg in recent:
    print(f"  - {msg.subject or '(no subject)'} from {msg.author_id.name}")
```

### Reports and Views

```python
# List all views
views = env['ir.ui.view'].search([])
print(f"Total views: {len(views)}")

# Count by type
view_types = env['ir.ui.view'].read_group(
    [],
    ['type'],
    ['type']
)
print("\nViews by type:")
for vt in view_types:
    print(f"  {vt['type']:15s}: {vt['type_count']}")

# List QWeb reports
reports = env['ir.actions.report'].search([])
print(f"\nQWeb reports: {len(reports)}")
for report in reports[:10]:
    print(f"  - {report.name} ({report.report_name})")
```

---

## Advanced Examples

### Performance Analysis

```python
import time

# Measure query performance
start = time.time()
partners = env['res.partner'].search([], limit=1000)
elapsed = time.time() - start
print(f"Loaded 1000 partners in {elapsed:.3f} seconds")

# Compare search vs search_count
start = time.time()
count1 = len(env['res.partner'].search([]))
time1 = time.time() - start

start = time.time()
count2 = env['res.partner'].search_count([])
time2 = time.time() - start

print(f"\nsearch: {count1} records in {time1:.3f}s")
print(f"search_count: {count2} records in {time2:.3f}s")
print(f"Speedup: {time1/time2:.2f}x")
```

### Data Analysis

```python
# Analyze partner distribution by country
env.cr.execute("""
    SELECT
        c.name as country,
        COUNT(p.id) as partner_count
    FROM res_partner p
    LEFT JOIN res_country c ON p.country_id = c.id
    WHERE p.country_id IS NOT NULL
    GROUP BY c.name
    ORDER BY partner_count DESC
    LIMIT 10
""")

print("Top 10 countries by partner count:")
for country, count in env.cr.fetchall():
    print(f"  {country:30s}: {count:5d} partners")

# Sales statistics (if sale module installed)
if 'sale.order' in env:
    env.cr.execute("""
        SELECT
            DATE_TRUNC('month', date_order) as month,
            COUNT(*) as order_count,
            SUM(amount_total) as total_amount
        FROM sale_order
        WHERE date_order >= NOW() - INTERVAL '6 months'
        GROUP BY month
        ORDER BY month DESC
    """)

    print("\nSales by month (last 6 months):")
    for month, count, total in env.cr.fetchall():
        print(f"  {month.strftime('%Y-%m')}: {count:4d} orders, ${total:,.2f}")
```

### Data Cleaning

```python
# Find duplicate partners by email
env.cr.execute("""
    SELECT
        email,
        COUNT(*) as count,
        ARRAY_AGG(id) as partner_ids
    FROM res_partner
    WHERE email IS NOT NULL AND email != ''
    GROUP BY email
    HAVING COUNT(*) > 1
    ORDER BY count DESC
    LIMIT 10
""")

print("Duplicate emails found:")
for email, count, ids in env.cr.fetchall():
    print(f"  {email}: {count} partners (IDs: {ids})")

# Find partners without email
no_email = env['res.partner'].search_count([
    ('email', '=', False),
    ('is_company', '=', False)
])
print(f"\nPartners without email: {no_email}")
```

### Bulk Operations

```python
# Update multiple records
partners = env['res.partner'].search([('phone', '=', False)], limit=10)
print(f"Updating {len(partners)} partners without phone...")

# Simulate update (uncomment to actually update)
# partners.write({'comment': 'Updated via Developer Terminal'})

print("Update complete!")

# Mass create (be careful!)
# Create test data
test_partners = []
for i in range(5):
    test_partners.append({
        'name': f'Test Partner {i+1}',
        'email': f'test{i+1}@example.com',
    })

# Uncomment to create
# created = env['res.partner'].create(test_partners)
# print(f"Created {len(created)} test partners")
```

### System Monitoring

```python
# Check cache statistics
cache_stats = env.registry.cache_hits
cache_total = env.registry.cache_hits + env.registry.cache_misses
if cache_total > 0:
    hit_rate = (cache_stats / cache_total) * 100
    print(f"Cache hit rate: {hit_rate:.2f}%")

# Check database size
env.cr.execute("""
    SELECT pg_size_pretty(pg_database_size(current_database()))
""")
db_size = env.cr.fetchone()[0]
print(f"Database size: {db_size}")

# Connection info
env.cr.execute("""
    SELECT
        COUNT(*) as connections,
        COUNT(*) FILTER (WHERE state = 'active') as active,
        COUNT(*) FILTER (WHERE state = 'idle') as idle
    FROM pg_stat_activity
    WHERE datname = current_database()
""")
total, active, idle = env.cr.fetchone()
print(f"\nDatabase connections:")
print(f"  Total: {total}")
print(f"  Active: {active}")
print(f"  Idle: {idle}")
```

---

## Tips and Best Practices

### 1. Always Test Safely
```python
# Use search_count before search for large datasets
count = env['res.partner'].search_count([])
if count > 10000:
    print(f"Warning: {count} records found, limiting to 100")
    records = env['res.partner'].search([], limit=100)
else:
    records = env['res.partner'].search([])
```

### 2. Use Transactions Carefully
```python
# Read operations are safe
partners = env['res.partner'].search([])

# Write operations affect the database
# Be very careful and test with small datasets first
# Consider using env.cr.rollback() if needed
```

### 3. Format Output Nicely
```python
# Use f-strings for formatting
for partner in env['res.partner'].search([], limit=5):
    print(f"{partner.id:5d} | {partner.name:30s} | {partner.email or 'N/A':30s}")

# Use pretty printing for complex data
import pprint
data = {'key': 'value', 'nested': {'a': 1, 'b': 2}}
pprint.pprint(data)
```

### 4. Handle Errors Gracefully
```python
try:
    result = env['res.partner'].search([('invalid_field', '=', 'value')])
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
```

---

## Security Reminders

- ⚠️ **Always test** commands in a development environment first
- ⚠️ **Be careful** with write/create/unlink operations
- ⚠️ **Never share** commands that contain passwords or sensitive data
- ⚠️ **Review** command history regularly
- ⚠️ **Use** appropriate access controls

---

**Happy coding! 🎉**
