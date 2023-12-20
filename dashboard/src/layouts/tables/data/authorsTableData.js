/* eslint-disable react/prop-types */
// Vision UI Dashboard React components
import VuiBox from "components/VuiBox";
import VuiTypography from "components/VuiTypography";
import VuiAvatar from "components/VuiAvatar";
import VuiBadge from "components/VuiBadge";

// Images
import avatar1 from "assets/images/avatar1.png";
import avatar2 from "assets/images/avatar2.png";
import avatar3 from "assets/images/avatar3.png";
import avatar4 from "assets/images/avatar4.png";
import avatar5 from "assets/images/avatar5.png";
import avatar6 from "assets/images/avatar6.png";

function Author({ image, name, email }) {
  return (
    <VuiBox display="flex" alignItems="center" px={1} py={0.5}>
      <VuiBox mr={2}>
        <VuiAvatar src={image} alt={name} size="sm" variant="rounded" />
      </VuiBox>
      <VuiBox display="flex" flexDirection="column">
        <VuiTypography variant="button" color="white" fontWeight="medium">
          {name}
        </VuiTypography>
        <VuiTypography variant="caption" color="text">
          {email}
        </VuiTypography>
      </VuiBox>
    </VuiBox>
  );
}

function Function({ job, org }) {
  return (
    <VuiBox display="flex" flexDirection="column">
      <VuiTypography variant="caption" fontWeight="medium" color="white">
        {job}
      </VuiTypography>
      <VuiTypography variant="caption" color="text">
        {org}
      </VuiTypography>
    </VuiBox>
  );
}

export default {
  columns: [
    { name: "client", align: "left" },
    { name: "company", align: "left" },
    { name: "status", align: "center" },
    { name: "date", align: "center" },
    { name: "income", align: "center" },
  ],

  rows: [
    {
      client: <Author image={avatar4} name="Esthera Jackson" email="esthera@simmmple.com" />,
      company: <Function job="Manager" org="Netflix" />,
      status: (
        <VuiBadge
          variant="standard"
          badgeContent="Done"
          color="success"
          size="xs"
          container
          sx={({ palette: { white, success }, borders: { borderRadius, borderWidth } }) => ({
            background: success.main,
            border: `${borderWidth[1]} solid ${success.main}`,
            borderRadius: borderRadius.md,
            color: white.main,
          })}
        />
      ),
      date: (
        <VuiTypography variant="caption" color="white" fontWeight="medium">
          23/04/18
        </VuiTypography>
      ),
      income: (
        <VuiTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
          $3200
        </VuiTypography>
      ),
    },
    {
      client: <Author image={avatar2} name="Alexa Liras" email="alexa@simmmple.com" />,
      company: <Function job="Programator" org="Stripe" />,
      status: (
        <VuiBadge
          variant="standard"
          badgeContent="Open"
          size="xs"
          container
          sx={({ palette: { white }, borders: { borderRadius, borderWidth } }) => ({
            background: "unset",
            border: `${borderWidth[1]} solid ${white.main}`,
            borderRadius: borderRadius.md,
            color: white.main,
          })}
        />
      ),
      date: (
        <VuiTypography variant="caption" color="white" fontWeight="medium">
          11/01/19
        </VuiTypography>
      ),
      income: (
        <VuiTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
          $500
        </VuiTypography>
      ),
    },
    {
      client: <Author image={avatar3} name="Laurent Michael" email="laurent@simmmple.com" />,
      company: <Function job="Executive" org="HubSpot" />,
      status: (
        <VuiBadge
          variant="standard"
          badgeContent="Done"
          color="success"
          size="xs"
          container
          sx={({ palette: { white, success }, borders: { borderRadius, borderWidth } }) => ({
            background: success.main,
            border: `${borderWidth[1]} solid ${success.main}`,
            borderRadius: borderRadius.md,
            color: white.main,
          })}
        />
      ),
      date: (
        <VuiTypography variant="caption" color="white" fontWeight="medium">
          19/09/17
        </VuiTypography>
      ),
      income: (
        <VuiTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
          $1280
        </VuiTypography>
      ),
    },
    {
      client: <Author image={avatar5} name="Daniel Thomas" email="daniel@simmmple.com" />,
      company: <Function job="Manager" org="Webflow" />,
      status: (
        <VuiBadge
        variant="standard"
        badgeContent="Pending"
        color="warning"
        size="xs"
        container
        sx={({ palette: { white, warning }, borders: { borderRadius, borderWidth } }) => ({
          background: warning.main,
          border: `${borderWidth[1]} solid ${warning.main}`,
          borderRadius: borderRadius.md,
          color: white.main,
        })}
      />
      ),
      date: (
        <VuiTypography variant="caption" color="white" fontWeight="medium">
          04/10/21
        </VuiTypography>
      ),
      income: (
        <VuiTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
          $900
        </VuiTypography>
      ),
    },
    {
      client: <Author image={avatar6} name="Mark Wilson" email="mark@simmmple.com" />,
      company: <Function job="Programtor" org="Apple" />,
      status: (
        <VuiBadge
          variant="standard"
          badgeContent="Open"
          size="xs"
          container
          sx={({ palette: { white }, borders: { borderRadius, borderWidth } }) => ({
            background: "unset",
            border: `${borderWidth[1]} solid ${white.main}`,
            borderRadius: borderRadius.md,
            color: white.main,
          })}
        />
      ),
      date: (
        <VuiTypography variant="caption" color="white" fontWeight="medium">
          14/09/20
        </VuiTypography>
      ),
      income: (
        <VuiTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
          $3000
        </VuiTypography>
      ),
    },
  ],
};
