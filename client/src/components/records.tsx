import {
  Table,
  TableCaption,
  TableRow,
  TableCell,
  TableHead,
  TableBody,
} from "@cmsgov/design-system";
import { useEffect, useState } from "react";

export type EOBRecord = {
  id: string;
  code: string;
  display: string;
  amount: number;
};

export type ErrorResponse = {
  type: string;
  content: string;
};

export default function Records() {
  const [records, setRecords] = useState<EOBRecord[]>([]);
  const [message, setMessage] = useState<ErrorResponse>();
  /*
   * DEVELOPER NOTES:
   *  Here we are parsing through the different PDE Claim records
   * for the user/beneficiary.  We have hard coded certain pieces of this data. (ie...item[0])
   * You will want to find a method of parsing the FHIR JSON response to get the data
   * you need for your application.  Don't forget to use a 'Discriminator' to determine
   * which item within a list you want to get data from.
   *
   * ie.  You are interested in getting all Prescription Drug NDC codes you would use the following criteria/discriminator
   * resource.item[N].coding[N].code WHERE resource.item[N].coding[N].system = "http://hl7.org/fhir/sid/ndc"
   *
   *
   * *NOTE*
   * There are multiple claim types within the BB2 Sandbox, not just PDE (Part-D Events - Drug/Medication Claims).  There are also
   * Carrier Claims, SNF, HHA, Hospice, Inpatient, and Outpatient
   */
  useEffect(() => {
    fetch("/api/data/benefit")
      .then((res) => {
        return res.json();
      })
      .then((eobData) => {
        if (eobData.entry) {
          const records: EOBRecord[] = eobData.entry.map(
            (resourceData: any) => {
              const resource = resourceData.resource;
              return {
                id: resource.id,
                code:
                  resource.item[0]?.productOrService?.coding[0]?.code ||
                  "Unknown",
                display:
                  resource.item[0]?.productOrService?.coding[0]?.display ||
                  "Unknown Prescription Drug",
                amount: resource.item[0]?.adjudication[7]?.amount?.value || "0",
              };
            }
          );
          setRecords(records);
        } else {
          if (eobData.message) {
            setMessage({
              type: "error",
              content: eobData.message || "Unknown",
            });
          }
        }
      });
  }, []);

  if (message) {
    return (
      <div className="full-width-card">
        <Table
          className="ds-u-margin-top--2"
          stackable
          stackableBreakpoint="md"
        >
          <TableCaption>Error Response</TableCaption>
          <TableHead>
            <TableRow>
              <TableCell id="column_1">Type</TableCell>
              <TableCell id="column_2">Content</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell stackedTitle="Type" headers="column_1">
                {message.type}
              </TableCell>
              <TableCell stackedTitle="Content" headers="column_2">
                {message.content}
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    );
  } else {
    return (
      <div className="full-width-card">
        <Table
          className="ds-u-margin-top--2"
          stackable
          stackableBreakpoint="md"
        >
          <TableCaption>Medicare Prescription Drug Claims Data</TableCaption>
          <TableHead>
            <TableRow>
              <TableCell id="column_1">NDC Code</TableCell>
              <TableCell id="column_2">Prescription Drug Name</TableCell>
              <TableCell id="column_3">Cost</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {records.map((record) => {
              return (
                <TableRow key={record.id}>
                  <TableCell stackedTitle="NDC Code" headers="column_1">
                    {record.code}
                  </TableCell>
                  <TableCell
                    stackedTitle="Prescription Drug Name"
                    headers="column_2"
                  >
                    {record.display}
                  </TableCell>
                  <TableCell stackedTitle="Cost" headers="column_3">
                    ${record.amount}.00
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </div>
    );
  }
}
