import React from "react";
import "antd/dist/antd.css";
import "./index.css";
import {
  Modal,
  Button,
  Input,
  Typography,
  Form,
  Select,
  DatePicker,
} from "antd";

const { Title } = Typography;
const { Option } = Select;

class App extends React.Component {
  state = { visible: false };

  showModal = () => {
    this.setState({
      visible: true,
    });
  };

  handleOk = (e) => {
    console.log(e);
    this.setState({
      visible: false,
    });
  };

  handleCancel = (e) => {
    console.log(e);
    this.setState({
      visible: false,
    });
  };

  render() {
    return (
      <>
        <Title>Independent Study</Title>
        <Button type="primary" onClick={this.showModal}>
          Get Sentiment Analysis
        </Button>
        <Modal
          title="Select Specifications"
          visible={this.state.visible}
          onOk={this.handleOk}
          onCancel={this.handleCancel}
          footer={false}
        >
          <Form
            labelCol={{ span: 4 }}
            wrapperCol={{ span: 14 }}
            layout="horizontal"
          >
            <Form.Item label="Ticker">
              <Input />
            </Form.Item>
            <Form.Item label="Data source">
              <Select>
                <Option value="twitter">Twitter</Option>
                <Option value="reddit">Reddit</Option>
                <Option value="10q">10Q</Option>
                <Option value="10k">10K</Option>
                <Option value="googleFinance">Google Finance</Option>
              </Select>
            </Form.Item>
            <Form.Item label="From">
              <DatePicker />
            </Form.Item>
            <Form.Item label="To">
              <DatePicker />
            </Form.Item>
            <Form.Item>
              <Button type="primary">Submit</Button>
            </Form.Item>
          </Form>
        </Modal>
      </>
    );
  }
}

export default App;
