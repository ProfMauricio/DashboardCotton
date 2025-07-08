import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


# Load the config
with open('./credentials.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
stauth.Hasher.hash_passwords(config['credentials'])

# Save the Hashed Credentials to our config file
with open('./credentials.yml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
try:
    auth = authenticator.login('main')
except Exception as e:
    st.error(e)

# All the authentication info is stored in the session_state
if st.session_state["authentication_status"]:
    # User is connected
    authenticator.logout('Logout', 'main')
    custo_producao_page = st.Page("dashboard_custo_producao.py", title="Custo de Produção",
                                  icon=":material/empty_dashboard:")

    # custo_

    pg = st.navigation([custo_producao_page, st.Page("dashboard_modelo1.py")])

    pg.run()
elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
    # Stop the rendering if the user isn't connected
    st.stop()
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
    # Stop the rendering if the user isn't connected
    st.stop()


st.title('🔐 Protected Application')
st.write(f'Welcome *{st.session_state["name"]}*')


